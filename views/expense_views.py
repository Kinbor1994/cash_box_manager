import sys

from views.generic import CreateView, UpdateView, ListView
from models import ExpenseCategoryModel, ExpenseModel
from controllers import ExpenseCategoryController, ExpenseController

class CreateExpenseCategory(CreateView):
    
    def __init__(self, title="Ajouter une Nouvelle Catégorie", model=ExpenseCategoryModel, controller=ExpenseCategoryController(), parent=None):
        super().__init__(title, model, controller, parent)
        
class UpdateExpenseCategory(UpdateView):
    def __init__(self, title="Modification de Catégorie", model=ExpenseCategoryModel, controller=ExpenseCategoryController(), id=None):
        super().__init__(title, model, controller, id)
        
class ExpenseCategoryList(ListView):
    
    def __init__(self, model=ExpenseCategoryModel,controller=ExpenseCategoryController()):
        super().__init__(model, controller)
        
class CreateExpense(CreateView):
    
    def __init__(self, title="Ajouter une Nouvelle Catégorie", model=ExpenseModel, controller=ExpenseController(), parent=None):
        super().__init__(title, model, controller, parent)
        
class UpdateExpense(UpdateView):
    def __init__(self, title="Modification de Catégorie", model=ExpenseModel, controller=ExpenseController(), id=None):
        super().__init__(title, model, controller, id)
        
class ExpenseList(ListView):
    
    def __init__(self, model=ExpenseModel,controller=ExpenseController()):
        super().__init__(model, controller)
        

if __name__ == "__main__":
    from imports import QApplication
    app = QApplication([])
    
    window = ExpenseList()
    window.show()
    
    sys.exit(app.exec())