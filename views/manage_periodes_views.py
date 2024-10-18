from views.generic import CreateView, UpdateView, ListView
from models.cash_box_period import CashBoxPeriod
from controllers.cash_box_controller import CashBoxPeriodController

class CashBoxPeriodCreateView(CreateView):
    
    def __init__(self, title="Ouverture d'un exercice.", model=CashBoxPeriod, controller=CashBoxPeriodController()):
        super().__init__(title, model, controller)
        
class CashBoxPeriodUpdateView(UpdateView):
    
    def __init__(self, title="Modification.", model=CashBoxPeriod, controller=CashBoxPeriodController(), id=None):
        super().__init__(title, model, controller, id)
        
class CashBoxPeriodList(ListView):
    
    def __init__(self, model=CashBoxPeriod, controller=CashBoxPeriodController()):
        super().__init__(model, controller)
        
if __name__ == "__main__":
    import sys
    from imports import QApplication
    app = QApplication([])
    
    window = CashBoxPeriodCreateView()
    window.show()
    
    sys.exit(app.exec())