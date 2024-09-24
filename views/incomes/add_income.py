import sys
from imports import QSize, QMessageBox

from pyside6_custom_widgets.labeled_line_edit import LabeledLineEdit
from views.base_add_view import BaseAddWidget

from controllers.income_controller import IncomeCategoryController
class AddIncome(BaseAddWidget):
    
    def __init__(self):
        super().__init__(title="Ajouter un Nouveau Revenu", fields=self.set_field_list(), controller=IncomeCategoryController())
        self.setGeometry(100,100,448, 250)
        self.setMinimumSize(QSize(448, 250))
        self.setMaximumSize(QSize(448, 250))
        
    def set_field_list(self):
        fields_list = []
        self.title_widget = LabeledLineEdit(label_text="Title",placeholder_text="Saisissez le title de la catégorie...",error_message="Ce champ est obligatoire",required=True)
        fields_list.append(self.title_widget)

        return fields_list
    
    def setup_connections(self):
        super().setup_connections()
        self.submit_btn.clicked.connect(self.on_submit)
        
    def on_submit(self):
        if self.validate_fields():
            self.add_income()
        else:
            QMessageBox.critical(self, "Error", "Vous devrez renseigner tous les champs.")
        
    def add_income(self):
        try:
            title = self.get_credentials()[0]
            category = self.controller.create(title=title)
            if category:
                QMessageBox.information(self, "Succes", f"La catégorie `{title}` à été créée avec succès.")
            else:
                QMessageBox.critical(self, "Succes", "Une erreur est survenue. Veuillez vérifier que vous avez bien rempli tout les champs et réessayez.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"{e}")
        
if __name__ == "__main__":
    from imports import QApplication
    app = QApplication([])
    
    window = AddIncome()
    window.show()
    
    sys.exit(app.exec())