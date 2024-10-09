from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from database.database import session
from controllers import BaseController

from models import ExpenseCategoryModel, ExpenseModel

class ExpenseCategoryController(BaseController):
    
    def __init__(self):
        super().__init__(model=ExpenseCategoryModel)
        
class ExpenseController(BaseController):
    
    def __init__(self):
        super().__init__(model=ExpenseModel)
    
    
    @property
    def get_total_expense(self):
        
        try:
            total = session.query(func.sum(self.model.amount)).scalar()
            return total if total is not None else 0.0
        except SQLAlchemyError as e:
            raise
        finally:
            session.close()
    