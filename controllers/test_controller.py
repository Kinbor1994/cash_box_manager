
from controllers.base_controller import BaseController, RecordNotFoundError
from models.incomes import IncomeCategoryModel, IncomeModel
from controllers.income_controller import IncomeController
from sqlalchemy.engine.row import Row
# class IncomeController(BaseController):
    
#     def __init__(self):
#         super().__init__(IncomeModel)
        
if __name__ == "__main__":
        controller = IncomeController()
        try:
            items = controller.get_filter_by_category_id(1)
            for elm in items:
                print(isinstance(elm, Row))
                print(f"{elm}")
        except RecordNotFoundError as e:
            print(f"Error: {e}")  # Affiche uniquement le message d'erreur
        except Exception as e:
            print(f"Unexpected error: {e}")