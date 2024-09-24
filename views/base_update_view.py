import sys
from pathlib import Path

from imports import QDialog, Signal, QSize, QVBoxLayout, QHBoxLayout, QFrame, QSpacerItem, QSizePolicy
from pyside6_custom_widgets.button import Button
from pyside6_custom_widgets.label import Label
from pyside6_custom_widgets.labeled_combobox_2 import LabeledComboBox
from pyside6_custom_widgets.labeled_date_edit import LabeledDateEdit
from pyside6_custom_widgets.labeled_line_edit import LabeledLineEdit
from utils.utils import  set_app_icon
from views.base_add_view import BaseAddWidget

class BaseUpdateWidget(BaseAddWidget):
    
    reload_signal = Signal()
    
    def __init__(self, title="", fields=[], controller=None, id=0):
        super().__init__(title, fields, controller)
        self.record_id = id
    
    def setup_ui(self):
        super().setup_ui()
        self.submit_btn.setText("Enregistrer")
        
    
if __name__ == "__main__":
    from imports import QApplication
    
    app = QApplication([])
    
    window = BaseUpdateWidget()
    window.show()
    
    sys.exit(app.exec())