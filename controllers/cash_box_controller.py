from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from database.database import session

from controllers.base_controller import BaseController, RecordNotFoundError
from controllers.expense_controller import ExpenseController
from controllers.income_controller import IncomeController

from models.cash_box_period import CashBoxPeriod

class CashBoxPeriodController(BaseController):
    
    def __init__(self):
        super().__init__(model=CashBoxPeriod)
        
    def close_period(self, id_, end_date=None):
        
        try:
            instance = session.query(self.model).filter(self.model.id == id_).first()
            if instance is None:
                raise RecordNotFoundError("Record not found.")
            initial_balance = instance.initial_amount
            total_expense = ExpenseController().get_total_expense
            total_income = IncomeController().get_total_income
            instance.end_date = end_date or datetime.now()
            instance.is_open = False
    
        except RecordNotFoundError:
            raise
        except SQLAlchemyError as e:
            raise
        finally:
            session.close()