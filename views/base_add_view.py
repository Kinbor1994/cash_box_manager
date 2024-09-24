import sys
from pathlib import Path

from imports import QDialog, Signal, QSize, QVBoxLayout, QHBoxLayout, QFrame, QSpacerItem, QSizePolicy
from pyside6_custom_widgets.button import Button
from pyside6_custom_widgets.label import Label
from pyside6_custom_widgets.labeled_combobox_2 import LabeledComboBox
from pyside6_custom_widgets.labeled_date_edit import LabeledDateEdit
from pyside6_custom_widgets.labeled_line_edit import LabeledLineEdit
from utils.utils import  set_app_icon

class BaseAddWidget(QDialog):
    
    reload_signal = Signal()
    
    def __init__(self, title="", fields=[], controller=None):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100,100,448, 400)
        self.setMinimumSize(QSize(448, 400))
        self.setMaximumSize(QSize(448, 400))
        set_app_icon(self)
        self.title = title
        self.fields = fields
        if controller:
            self.controller = controller
        self.setup_ui()
        
        self.setup_connections()
    
    def setup_ui(self):
        self.main_layout = QVBoxLayout()

        self.title_label = Label(text=self.title)
        self.title_label.setProperty("role","page_title")
        self.main_layout.addWidget(self.title_label)

        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        self.main_layout.addWidget(self.separator)
        
        self.set_field(self.fields) 
        
        self.button_layout = QHBoxLayout()
        self.submit_btn = Button(text="Ajouter", icon_name="fa.save", theme_color="primary")
        self.cancel_btn = Button(text="Retour", icon_name="fa.sign-out", theme_color="danger")
        
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.button_layout.addItem(spacer)

        self.button_layout.addWidget(self.submit_btn)
        self.button_layout.addWidget(self.cancel_btn)

        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)
    
    def set_field(self, fields_list=[]):
        for field in fields_list:
            self.main_layout.addWidget(field)
    
    def setup_connections(self):
        self.cancel_btn.clicked.connect(self.close)
    
    def validate_fields(self):
        """
        Validates the fields dynamically and highlights any empty or invalid fields with a red border.
        """
        all_valid = True
        
        for field in self.fields:
            all_valid = field.is_valid()
            
        return all_valid

    def get_credentials(self):
        """
        Dynamically retrieves the input values if all fields are valid.

        Returns:
            list: A list containing the values of all valid fields.
        """
        credentials = []

        for widget_type in [LabeledLineEdit, LabeledComboBox, LabeledDateEdit]:
            widgets = self.findChildren(widget_type)
            for widget in widgets:
                credentials.append(widget.get_value())
                
        return credentials if self.validate_fields() else None

    
    def closeEvent(self,event):
        super().closeEvent(event)
        self.reload_signal.emit()
    
if __name__ == "__main__":
    from imports import QApplication
    
    app = QApplication([])
    
    window = BaseAddWidget()
    window.title_label.set_text("Ajouter un Revenu")
    window.show()
    
    sys.exit(app.exec())