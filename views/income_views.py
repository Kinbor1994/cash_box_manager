import sys

from pyside6_custom_widgets.labeled_combobox_2 import LabeledComboBox
from views.generic import CreateView, UpdateView, ListView
from models import IncomeCategoryModel, IncomeModel
from controllers import IncomeCategoryController, IncomeController

class CreateIncomeCategory(CreateView):
    
    def __init__(self, title="Ajouter une Nouvelle Catégorie", model=IncomeCategoryModel, controller=IncomeCategoryController(), parent=None):
        super().__init__(title, model, controller, parent)
        
class UpdateIncomeCategory(UpdateView):
    def __init__(self, title="Modification de Catégorie", model=IncomeCategoryModel, controller=IncomeCategoryController(), id=None):
        super().__init__(title, model, controller, id)
        
class IncomeCategoryList(ListView):
    
    def __init__(self, model=IncomeCategoryModel,controller=IncomeCategoryController()):
        super().__init__(model, controller)
        
class CreateIncome(CreateView):
    
    def __init__(self, title="Ajouter une Nouvelle Catégorie", model=IncomeModel, controller=IncomeController(), parent=None):
        super().__init__(title, model, controller, parent)
        
class UpdateIncome(UpdateView):
    def __init__(self, title="Modification de Catégorie", model=IncomeModel, controller=IncomeController(), id=None):
        super().__init__(title, model, controller, id)
        
class IncomeList(ListView):
    
    def __init__(self, model=IncomeModel,controller=IncomeController()):
        super().__init__(model, controller)
        

if __name__ == "__main__":
    from imports import QApplication
    app = QApplication([])
    
    window = CreateIncome()
    window.show()
    
    sys.exit(app.exec())