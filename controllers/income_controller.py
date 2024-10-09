from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from database.database import session
from controllers.base_controller import BaseController

from models.incomes import IncomeCategoryModel, IncomeModel

class IncomeCategoryController(BaseController):
    
    def __init__(self):
        super().__init__(model=IncomeCategoryModel)
        
class IncomeController(BaseController):
    
    def __init__(self):
        super().__init__(model=IncomeModel)
        
    @property
    def get_total_income(self):
        
        try:
            total = session.query(func.sum(self.model.amount)).scalar()
            return total if total is not None else 0.0
        except SQLAlchemyError as e:
            raise
        finally:
            session.close()
    