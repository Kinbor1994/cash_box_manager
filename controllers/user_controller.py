from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from database.database import get_session
from models.user import User
from utils.hashing import hash_text, verify_hashed_text

class UserController:
    def __init__(self):
        self.model = User

    def create_user(self, username: str, password: str, secret_question: str, secret_answer: str):
        """
        Create a new user secret question and answer.
        """
        try:
            with get_session() as session:
                user = self.model(
                    username=username,
                    password=hash_text(password),
                    secret_question=secret_question,
                    secret_answer=hash_text(secret_answer)
                )
                session.add(user)
                session.commit()
                return user
        except IntegrityError:
            session.rollback()
            raise
        except SQLAlchemyError as e:
            raise e

    def authenticate_user(self, username: str, password: str):
        """
        Authenticate a user with their username and password.
        """
        try:
            with get_session() as session:
                user = session.query(self.model).filter(self.model.username == username).first()
                if user:
                    return verify_hashed_text(password, user.password)
                return False
        except SQLAlchemyError as e:
            raise e

    def change_password(self, username: str, new_password: str):
        """
        Change the password for an existing user.
        """
        try:
            with get_session() as session:
                user = session.query(self.model).filter(self.model.username == username).first()
                if not user:
                    return False
                else:
                    user.password = hash_text(new_password)
                    session.commit()
                    return True
        except SQLAlchemyError as e:
            raise e

    def set_secret_question(self, username: str, question: str, answer: str):
        """
        Set the secret question and answer for a user.
        """
        try:
            with get_session() as session:
                user = session.query(self.model).filter(self.model.username == username).first()
                if user:
                    user.secret_question = question
                    user.secret_answer = hash_text(answer)
                    session.commit()
                    return True
                return False
        except SQLAlchemyError as e:
            raise e

    def verify_secret_answer(self, username: str, answer: str):
        """
        Verify the secret answer for a user.
        """
        try:
            with get_session() as session:
                user = session.query(self.model).filter(self.model.username == username).first()
                if user and verify_hashed_text(answer, user.secret_answer):
                    return True
                return False
        except SQLAlchemyError as e:
            raise e
        
    def get_secret_question(self, username: str):
        """
        Returns the secret question for a entered username.
        """
        try:
            with get_session() as session:
                user = session.query(self.model).filter(self.model.username == username).first()
                if user:
                    return str(user.secret_question)
                return ""
        except SQLAlchemyError as e:
            raise e

    def reset_password(self, username: str, new_password: str, answer: str):
        """
        Reset the password for a user after verifying the secret answer.
        """
        try:
            if self.verify_secret_answer(username, answer):
                with get_session() as session:
                    user = session.query(self.model).filter(self.model.username == username).first()
                    if user:
                        user.password = hash_text(new_password)
                        session.commit()
                        return True
            return False
        except SQLAlchemyError as e:
            raise e

    def get_user(self, username:str):
        
        try:
            with get_session() as session:
                user = session.query(self.model).filter(self.model.username == username).first()
                return user.id, user.username
        except SQLAlchemyError as e:
            raise e
        
    