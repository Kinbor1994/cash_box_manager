from pyside6_custom_widgets.button import Button
from imports import QWidget, QHBoxLayout

class ActionButtonsWidget(QWidget):
    def __init__(self, modify_callback=None, delete_callback=None, parent=None):
        super().__init__()
        self.setFixedHeight(40)
        self.setFixedWidth(85)
        self.modify_button = Button("",theme_color="primary",icon_name='fa.edit')
        self.delete_button = Button("",theme_color="danger",icon_name='fa5s.trash-alt')
        # Only connect the buttons if the callbacks exist
        if modify_callback:
            self.modify_button.clicked.connect(modify_callback)
        
        if delete_callback:
            self.delete_button.clicked.connect(delete_callback)
        
        # Layout setup
        layout = QHBoxLayout()
        layout.addWidget(self.modify_button)
        layout.addWidget(self.delete_button)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
    
class ActionButtonsWidget2(QWidget):
    def __init__(self, modify_callback=None, delete_callback=None, other_action_callback=None, parent=None):
        super().__init__()
        self.setFixedHeight(40)
        self.setFixedWidth(125)
        self.modify_button = Button("",theme_color="primary",icon_name='fa.edit')
        self.delete_button = Button("",theme_color="danger",icon_name='fa5s.trash-alt')
        self.other_action = Button("",theme_color="success",icon_name='fa5s.close-circle')
        # Only connect the buttons if the callbacks exist
        if modify_callback:
            self.modify_button.clicked.connect(modify_callback)
        
        if delete_callback:
            self.delete_button.clicked.connect(delete_callback)
        
        if other_action_callback:
            self.other_action.clicked.connect(other_action_callback)
        # Layout setup
        layout = QHBoxLayout()
        layout.addWidget(self.modify_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.other_action)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)