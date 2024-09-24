
from controllers.base_controller import BaseController, RecordNotFoundError
from models.incomes import IncomeCategoryModel, IncomeModel

class IncomeController(BaseController):
    
    def __init__(self):
        super().__init__(IncomeModel)
        
if __name__ == "__main__":
        controller = IncomeController()
        try:
            # c = controller.get_by_id(1)
            # for column in IncomeModel.__table__.columns:
            #     if column.info.get("editable",False) == "false":
            #         print(f"{column.info.get("editable")}")
            # print(c.category)
            items = controller.get_related_model_all("category_id")
            for elm in items:
                print(f"{elm.id} - {elm.title}")
        except RecordNotFoundError as e:
            print(f"Error: {e}")  # Affiche uniquement le message d'erreur
        except Exception as e:
            print(f"Unexpected error: {e}")