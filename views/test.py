import sys
from imports import QWidget
from controllers.income_controller import IncomeCategoryController, IncomeController
from models.incomes import IncomeCategoryModel, IncomeModel

from views.base_form_widget import BaseFormWidget


class TestGenForm(BaseFormWidget):
    
    def __init__(self, title="Test de Classe", model=IncomeModel, controller=IncomeController(), instance=None, parent=None):
        super().__init__(title, model, controller, instance, parent)
    
        
        
if __name__ == "__main__":
    from imports import QApplication
    
    app = QApplication([])
    
    window = TestGenForm()
    window.show()
    
    sys.exit(app.exec())