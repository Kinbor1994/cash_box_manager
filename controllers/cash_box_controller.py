from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
from database.database import session

from controllers.base_controller import BaseController, RecordNotFoundError
from controllers.expense_controller import ExpenseController
from controllers.income_controller import IncomeController

from models.cash_box_period import CashBoxPeriod
from utils.utils import read_config_file_data, read_id_from_file

user_id = read_config_file_data()["user_id"]

class CashBoxPeriodController(BaseController):
    
    def __init__(self):
        super().__init__(model=CashBoxPeriod)
            
    def get_all(self):
        """
        Fetch all records with optional ordering.

        Returns:
            A list of model instances, ordered if applicable.
        """
        try:
            query = session.query(self.model)

            # Récupérer les colonnes avec 'order_column' dans leur 'info'
            order_columns = self._get_order_columns()
            # Appliquer l'ordre si des colonnes sont spécifiées
            if order_columns:
                query = query.order_by(*order_columns)

            return query.all()
        except SQLAlchemyError as e:
            raise
        finally:
            session.close()
    
    def calculate_ending_balance(self):
        """
        Calculate the ending balance for the current period.

        Returns:
            float: The ending balance of the current cash box period.
        """
        total_expense = ExpenseController().get_total_expense
        total_income = IncomeController().get_total_income
        
        end_balance = float(self.get_initial_balance) + total_income - total_expense
        return end_balance 
    
    @property
    def get_initial_balance(self):
        try:
            instance = session.query(self.model).filter(self.model.id == read_id_from_file()).first()
            if instance is None:
                return 0
            initial_balance = instance.initial_amount

            return initial_balance 
    
        except RecordNotFoundError:
            raise
        except SQLAlchemyError as e:
            raise
        finally:
            session.close()