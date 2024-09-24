import logging
from sqlalchemy.inspection import inspect
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from datetime import datetime

from database.database import session
from models.audit_model import AuditLog
from utils.utils import read_config_file_data

# Configurer le logger pour capturer les erreurs SQLAlchemy
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

user_id = read_config_file_data()["user_id"]

class ActionLogger:
    """
    A logger class to log actions performed on the database for non-repudiation.
    """
    def __init__(self):
        """
        Initialize the logger with a model to store log entries.

        Args:
            log_model (Type[Base]): The SQLAlchemy model class for logging actions.
        """
        self.log_model = AuditLog

    def log(self, action, user_id, table_name, record_id, description=None):
        """
        Log an action performed on a record.

        Args:
            action (str): The type of action (e.g., 'create', 'update', 'delete').
            user_id (int): The ID of the user performing the action.
            table_name (str): The name of the table affected.
            record_id (int): The ID of the affected record.
            description (str, optional): A description or details about the action.
        """
        
        try:
            log_entry = self.log_model(
                action=action,
                user_id=user_id,
                table_name=table_name,
                record_id=record_id,
                description=description,
            )
            session.add(log_entry)
            session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Failed to log action: {e}")
            session.rollback()
            raise
        finally:
            session.close()

class BaseController:
    """
    A generic controller class for managing CRUD operations with SQLAlchemy.

    Attributes:
        model (Type[Base]): The SQLAlchemy model class associated with this controller.
        action_logger (ActionLogger): The logger to record database actions.
    """

    def __init__(self, model):
        """
        Initialize the BaseController with a specific SQLAlchemy model and a logger.

        Args:
            model (Type[Base]): The SQLAlchemy model class to use with this controller.
            log_model (Type[Base]): The SQLAlchemy model class for logging actions.
        """
        self.model = model
        self.action_logger = ActionLogger()

    def create(self, **kwargs):
        """
        Create a new record in the database.

        Args:
            user_id (int): The ID of the user performing the action.
            **kwargs: Field values for the new record.

        Returns:
            The created record instance.

        Raises:
            RecordAlreadyExistsError: If a record with the same unique fields already exists.
            SQLAlchemyError: For any SQLAlchemy-related errors.
        """
        
        try:
            instance = self.model(**kwargs)
            session.add(instance)
            session.commit()
            self.action_logger.log('create', user_id, self.model.__tablename__, instance.id, description=f"Created record with values {kwargs}")
            return instance
        except IntegrityError:
            session.rollback()
            raise RecordAlreadyExistsError("A record with the provided information already exists.")
        except SQLAlchemyError as e:
            session.rollback()
            raise
        finally:
            session.close()

    def get_by_id(self, id_):
        """
        Retrieve a record by its ID.

        Args:
            id_ (int): The ID of the record to retrieve.

        Returns:
            The record instance with the specified ID.

        Raises:
            RecordNotFoundError: If no record with the specified ID is found.
            SQLAlchemyError: For any SQLAlchemy-related errors.
        """
        
        try:
            instance = session.query(self.model).filter(self.model.id == id_).first()
            if instance is None:
                raise RecordNotFoundError("Record not found.")
            return instance
        except RecordNotFoundError:
            raise
        except SQLAlchemyError as e:
            raise
        finally:
            session.close()

    def update(self, id_, **kwargs):
        """
        Update an existing record with new values.

        Args:
            id_ (int): The ID of the record to update.
            **kwargs: New field values for the record.

        Returns:
            The updated record instance.

        Raises:
            RecordNotFoundError: If no record with the specified ID is found.
            SQLAlchemyError: For any SQLAlchemy-related errors.
        """
        
        try:
            instance = session.query(self.model).filter(self.model.id == id_).first()
            if instance is None:
                raise RecordNotFoundError("Record not found.")

            for key, value in kwargs.items():
                setattr(instance, key, value)

            session.commit()
            self.action_logger.log('update', user_id, self.model.__tablename__, id_, description=f"Updated record with values {kwargs}")
            return instance
        except RecordNotFoundError:
            session.rollback()
            raise
        except SQLAlchemyError as e:
            session.rollback()
            raise
        finally:
            session.close()

    def delete(self, id_):
        """
        Delete a record by its ID.

        Args:
            id_ (int): The ID of the record to delete.

        Returns:
            bool: True if the record was deleted successfully, False otherwise.

        Raises:
            RecordNotFoundError: If no record with the specified ID is found.
            SQLAlchemyError: For any SQLAlchemy-related errors.
        """
        
        try:
            instance = session.query(self.model).filter(self.model.id == id_).first()
            if instance is None:
                raise RecordNotFoundError("Record not found.")

            session.delete(instance)
            session.commit()
            self.action_logger.log('delete', user_id, self.model.__tablename__, id_)
            return True
        except RecordNotFoundError:
            session.rollback()
            raise
        except SQLAlchemyError as e:
            session.rollback()
            raise
        finally:
            session.close()
    
    def get_all(self):
        """
        Fetch all records.

        Returns:
            A list of model instances.
        """
        
        try:
            if hasattr(self.model, 'query_ordered'):
                query = self.model.query_ordered(session)
            else:
                query = session.query(self.model)
            return query.all()
        except SQLAlchemyError as e:
            raise
        finally:
            session.close()

    def search(self, **filters):
        """
        Search records based on multiple filters.

        Args:
            filters: Key-value pairs to filter records.

        Returns:
            A list of model instances that match the filters.
        """
        
        try:
            query = session.query(self.model)
            for key, value in filters.items():
                if hasattr(self.model, key):
                    query = query.filter(getattr(self.model, key) == value)
            return query.all()
        except SQLAlchemyError as e:
            raise
        finally:
            session.close()
    
    def get_related_model(self, foreign_key_column_name):
        """
        Retrieve the related model dynamically based on a ForeignKey column.
        
        Args:
            foreign_key_column_name (str): The column name holding the ForeignKey.
        
        Returns:
            The related model class.
        """
        mapper = inspect(self.model)
        
        for prop in mapper.relationships:
            for col in prop.local_columns:
                if col.name == foreign_key_column_name:
                    return prop.mapper.class_
        
    def get_related_model_all(self, foreign_key_column_name):
        
        try:
            related_model = self.get_related_model(foreign_key_column_name)
            if related_model:
                return session.query(related_model).outerjoin(self.model).all()
        except SQLAlchemyError as e:
            raise
        finally:
            session.close()
            
class RecordNotFoundError(Exception):
    """Exception raised when a record is not found."""
    pass

class RecordAlreadyExistsError(Exception):
    """Exception raised when attempting to create a record that already exists."""
    pass


