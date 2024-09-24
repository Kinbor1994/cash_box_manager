
from controllers.base_controller import BaseController

from models.incomes import IncomeCategoryModel, IncomeModel

class IncomeCategoryController(BaseController):
    
    def __init__(self):
        super().__init__(model=IncomeCategoryModel)
        
class IncomeController(BaseController):
    
    def __init__(self):
        super().__init__(model=IncomeModel)