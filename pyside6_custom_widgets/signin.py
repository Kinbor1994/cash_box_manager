from pyside6_custom_widgets.button import Button
from pyside6_custom_widgets.labeled_line_edit import LabeledLineEdit
from imports import QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QApplication,QSize
from qt_material import apply_stylesheet

class SignIn(QDialog):
    """
    A dialog for user sign-in with username and password fields.

    Args:
        parent (QWidget, optional): The parent widget. Defaults to None.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sign In")
        self.setGeometry(100,100,300, 200)
        self.setMinimumSize(QSize(300, 200))
        self.setMaximumSize(QSize(300, 200))
        self.setup_ui()
        # apply_stylesheet(app, theme='dark_amber.xml')

    def setup_ui(self):
        """
        Sets up the user interface of the sign-in dialog.
        """
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(5, 5, 5, 5)
        # Username field
        self.username_field = LabeledLineEdit("Username:", placeholder_text="Enter your username", required=True)
        layout.addWidget(self.username_field)

        # Password field
        self.password_field = LabeledLineEdit("Password:", placeholder_text="Enter your password", required=True)
        self.password_field.line_edit.line_edit.setEchoMode(QLineEdit.Password)  # Mask the password
        layout.addWidget(self.password_field)

        # Buttons
        button_layout = QHBoxLayout()
        self.connect_button = Button(text="Connect",icon_name="fa5s.home",theme_color="primary")
        self.cancel_button = Button(text="Cancel",icon_name="fa5s.sign-out-alt",theme_color="danger")
        button_layout.addWidget(self.connect_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        layout.addStretch(1)
        # Connect button click to validation
        self.connect_button.clicked.connect(self.validate_fields)
        self.cancel_button.clicked.connect(self.close)
        
    def validate_fields(self):
        """
        Validates the fields and highlights any empty fields with a red border.
        """
        fields = [self.username_field, self.password_field]
        all_valid = True

        for field in fields:
            if not field.is_valid():
                field.line_edit.setStyleSheet("border: 2px solid red;")
                all_valid = False
            else:
                field.line_edit.setStyleSheet("")  # Reset to default

        return all_valid

    def get_credentials(self):
        """
        Returns the entered username and password if the input is valid.

        Returns:
            tuple: A tuple containing the username and password if valid, otherwise (None, None).
        """
        if self.validate_fields():
            return self.username_field.get_text(), self.password_field.get_text()
        else:
            return None, None

if __name__ == "__main__":
    app = QApplication([])

    window = SignIn()
    window.resize(300, 400)
    window.show()

    app.exec()
