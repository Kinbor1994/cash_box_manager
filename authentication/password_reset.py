from pathlib import Path
from controllers.user_controller import UserController
from pyside6_custom_widgets.button import Button
from pyside6_custom_widgets.labeled_line_edit import LabeledLineEdit
from imports import QDialog, QVBoxLayout, QLineEdit, QHBoxLayout, QIcon, QApplication,QSize, QMessageBox
from qt_material import apply_stylesheet

from utils.utils import set_app_icon

class ResetPassword(QDialog):
    """
    A dialog to ret password.

    Args:
        username (str): The username to reset the password.
    """

    def __init__(self, username:str):
        super().__init__()
        self.setWindowTitle("Changement de mot de passe")
        set_app_icon(self)
        self.setGeometry(100,100,400, 220)
        self.setMinimumSize(QSize(400, 220))
        self.setMaximumSize(QSize(400, 220))
        self.controller = UserController()
        self.username = username
        self.setup_ui()
        self.setup_connection()
        apply_stylesheet(self, theme='dark_amber.xml')

    def setup_ui(self):
        """
        Sets up the user interface of the password reset dialog.
        """
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Password field
        self.password_widget = LabeledLineEdit("Nouveau mot de passe:", placeholder_text="Entrez un nouveau mot de passe...", required=True)
        self.password_widget.line_edit.line_edit.setEchoMode(QLineEdit.Password)  # Mask the password
        layout.addWidget(self.password_widget)
        
        # Confirm Password field
        self.confirm_password_widget = LabeledLineEdit("Confirmer mot de passe:", placeholder_text="Confirmez le mot de passe...", required=True)
        self.confirm_password_widget.line_edit.line_edit.setEchoMode(QLineEdit.Password)  # Mask the password
        layout.addWidget(self.confirm_password_widget)

        # Buttons
        button_layout = QHBoxLayout()
        self.submit_button = Button(text="Envoyez",icon_name="fa.sign-in",theme_color="primary")
        self.cancel_button = Button(text="Retour",icon_name="fa.sign-out",theme_color="danger")
        
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        layout.addStretch(1)
    
    
    def setup_connection(self):
        self.submit_button.clicked.connect(self.on_submit)
        self.cancel_button.clicked.connect(self.close)
        
    def validate_fields(self):
        """
        Validates the fields and highlights any empty fields with a red border.
        """
        fields = [self.password_widget.line_edit, self.confirm_password_widget.line_edit]
        all_valid = True

        for field in fields:
            if not field.is_valid():
                field.line_edit.setStyleSheet("border: 2px solid red;")
                all_valid = False
            else:
                if self.password_widget.line_edit.get_text() == self.confirm_password_widget.line_edit.get_text():
                    field.line_edit.setStyleSheet("")  
                else:
                    field.line_edit.setStyleSheet("border: 2px solid red;")
                    all_valid = False
                    QMessageBox.warning(self, "Error", "Les mot de passes doivent être conforme.")

        return all_valid

    def get_credentials(self):
        """
        Returns the entered password if the input is valid.

        Returns:
            str: A string of the entered password if valid, otherwise None.
        """
        if self.validate_fields():
            return self.password_widget.get_text()
        else:
            return None

    def on_submit(self):
        if self.validate_fields():
            self.reset()
        else:
            QMessageBox.critical(self, "Error", "Les mot de passes doivent être conforme.")
            
    def reset(self):
        try:
            password = self.get_credentials()
            is_changed = self.controller.change_password(self.username, password)
            if is_changed :
                self.open_login()
            else:
                QMessageBox.critical(self,"Error","Votre mot de passe n'a pas été changé. Veuillez réessayer plus tard.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {e}")
        
    def open_login(self):
        from authentication.sign_in import SignIn
        self.signin = SignIn() 
        self.signin.show()
        self.close()
        
if __name__ == "__main__":
    app = QApplication([])

    window = ResetPassword("Borel")
    window.show()

    app.exec()
