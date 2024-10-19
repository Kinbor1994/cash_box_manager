from imports import QMessageBox

from views.generic import CreateView, UpdateView, ListView
from models.cash_box_period import CashBoxPeriod
from controllers.cash_box_controller import CashBoxPeriodController

class CashBoxPeriodCreateView(CreateView):
    def __init__(self):
        super().__init__(title="Ouvrir un exercice", model=CashBoxPeriod, controller=CashBoxPeriodController())
        
    def submit(self):
        """
        Handle form submission for both adding and editing.
        """
        try:
            form_data = self.get_form_data()
            if self.validate_fields():
                self.controller.create(**form_data)
                
                QMessageBox.information(self, "Success", "Opération effectuée avec succès.")
                self.clear_fieds()
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Vous devez correctement renseigner tous les champs importants.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Une erreur est survenue: \n{str(e)}")
        
class CashBoxPeriodUpdateView(UpdateView):
    
    def __init__(self, title="Modification.", model=CashBoxPeriod, controller=CashBoxPeriodController(), id=None):
        super().__init__(title, model, controller, id)

    def submit(self):
        """
        Handle form submission for editing an existing record.
        """
        try:
            form_data = self.get_form_data()
            if self.validate_fields():
                if form_data.get('is_open') == 'Fermé':
                    response = QMessageBox.question(self, "Confirmation de fermerture d'exercice", "Cet exercice va à présent être fermé. Continuer?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if response == QMessageBox.Yes:
                        form_data["ending_balance"] = self.controller.calculate_ending_balance()
                    elif response == QMessageBox.No:
                        return
                self.controller.update(id_=self.id, **form_data)  
                self.refresh_signal.emit()
                QMessageBox.information(self, "Success", "Données mises à jour avec succès.")
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Vous devez correctement renseigner tous les champs importants.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Une erreur est survenue: \n{str(e)}")
    
    def get_form_data(self):
        """
        Retrieve the data entered in the form.
        """
        data = {}
        for field in self.fields:
            column_name = field.objectName()
            data[column_name] = field.get_value()
    
        return data        

class CashBoxPeriodList(ListView):
    
    def __init__(self, model=CashBoxPeriod, controller=CashBoxPeriodController()):
        super().__init__(model, controller)

    def create_instance(self):
        create_form = CashBoxPeriodCreateView()
        create_form.refresh_data_signal.connect(self.refresh_data)
        create_form.exec()
        
    def edit_row(self, instance_id):
        """
        Edits the data of a specific row by invoking the controller.
        """
        edit_form = CashBoxPeriodUpdateView(id=instance_id)
        edit_form.refresh_signal.connect(self.refresh_data)
        edit_form.exec()
        
if __name__ == "__main__":
    import sys
    from imports import QApplication
    app = QApplication([])
    
    window = CashBoxPeriodList()
    window.show()
    
    sys.exit(app.exec())