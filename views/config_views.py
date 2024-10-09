from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from imports import QDialog, QHBoxLayout, QVBoxLayout, QMessageBox, QSize
from pyside6_custom_widgets.button import Button
from pyside6_custom_widgets.labeled_line_edit import LabeledLineEdit
from qt_material import apply_stylesheet

from utils.utils import set_app_icon, set_init_balance_data, get_initial_balance

class ConfigForm(QDialog):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Définir le solde initial")
        self.setGeometry(100,100,300, 150)
        self.setMinimumSize(QSize(300, 150))
        self.setMaximumSize(QSize(300, 150))
        apply_stylesheet(self, theme="default_light.xml")
        set_app_icon(self)
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        self.main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        self.solde_widget = LabeledLineEdit(label_text="Solde initial", required=True, input_type="numeric")
        self.solde_widget.set_value(get_initial_balance().get("solde", "0.0"))
        self.submit_btn = Button(text="Enregistrer", icon_name="fa.save", theme_color="success", command=None)
        self.cancel_btn = Button(text="Fermer", icon_name="fa.close", theme_color="danger", command=None)
        self.main_layout.addWidget(self.solde_widget)
        button_layout.addWidget(self.submit_btn)
        button_layout.addWidget(self.cancel_btn)
        self.main_layout.addLayout(button_layout)
        self.setLayout(self.main_layout)
        
    def set_init_solde(self):
        if self.solde_widget.is_valid():
            set_init_balance_data(float(self.solde_widget.get_value()))
            QMessageBox.information(self, "Success", "Solde initiale définit avec succès.")
            self.close()
    
    def setup_connections(self):
        self.submit_btn.clicked.connect(self.set_init_solde)
        self.cancel_btn.clicked.connect(self.close)
        
if __name__ == "__main__":
    import sys
    from imports import QApplication
    app = QApplication([])
    win = ConfigForm()
    win.show()
    sys.exit(app.exec())