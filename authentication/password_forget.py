from pathlib import Path

from authentication.password_reset import ResetPassword
from controllers.user_controller import UserController
from pyside6_custom_widgets.button import Button
from pyside6_custom_widgets.labeled_line_edit import LabeledLineEdit
from pyside6_custom_widgets.label import Label
from imports import QDialog, QVBoxLayout, QHBoxLayout, QIcon, QApplication,QSize, QMessageBox, QFrame

from qt_material import apply_stylesheet

from utils.utils import  set_app_icon
from main import MainWindow

class PasswordForget(QDialog):
    """
    A dialog to initiate password reset.

    Args:
        username (str): The username to reset the password.
    """

    def __init__(self, username:str):
        super().__init__()
        self.setWindowTitle("CASH BOX MANAGER BY BOREL")
        set_app_icon(self)
        self.setGeometry(100,100,400, 300)
        self.setMinimumSize(QSize(400, 300))
        self.setMaximumSize(QSize(400, 300))
        self.controller = UserController()
        self.username = username
        self.setup_ui()
        self.get_secret_question()
        self.setup_connection()
        apply_stylesheet(self, theme="default_light.xml")

    def setup_ui(self):
        """
        Sets up the user interface of the password forget dialog.
        """
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Secrete question
        self.secret_question_label = Label("")
        layout.addWidget(self.secret_question_label)
        
        # Password field
        self.secret_answer_widget = LabeledLineEdit("Réponse:", placeholder_text="Entrez votre réponse secrète...", required=True)
        layout.addWidget(self.secret_answer_widget)

        # Buttons
        button_layout = QHBoxLayout()
        self.submit_button = Button(text="Envoyez",icon_name="fa.sign-in",theme_color="primary")
        self.cancel_button = Button(text="Retour",icon_name="fa.sign-out",theme_color="danger")
        
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        #Separator
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(self.separator)
        
        #Signup or Login
        self.signup_button = Button(text="Creez un compte ici...",theme_color="info")
        self.login_button = Button(text="Connectez-vous...",theme_color="info")
        self.infos_label = Label(text="Ou")
        layout.addWidget(self.signup_button)
        layout.addWidget(self.infos_label)
        layout.addWidget(self.login_button)
        self.setLayout(layout)
        layout.addStretch(1)
    
    
    def setup_connection(self):
        self.submit_button.clicked.connect(self.on_submit)
        self.cancel_button.clicked.connect(self.close)
        self.login_button.clicked.connect(self.open_login)
        self.signup_button.clicked.connect(self.open_sinup)
        
    def validate_fields(self):
        """
        Validates the fields and highlights any empty fields with a red border.
        """
        fields = [self.secret_answer_widget.line_edit]
        all_valid = True

        for field in fields:
            if not field.is_valid():
                field.line_edit.setStyleSheet("border: 2px solid red;")
                all_valid = False
            else:
                field.line_edit.setStyleSheet("")  

        return all_valid

    def get_credentials(self):
        """
        Returns the entered secret answer if the input is valid.

        Returns:
            str: A string of the secret answer if valid, otherwise None.
        """
        if self.validate_fields():
            return self.secret_answer_widget.get_text()
        else:
            return None

    def on_submit(self):
        if self.validate_fields():
            self.reset()
        else:
            QMessageBox.critical(self, "Error", "Vous devrez renseigner tous les champs.")
            
    def reset(self):
        try:
            answer = self.get_credentials()
            is_valid_answer = self.controller.verify_secret_answer(self.username, answer)
            if is_valid_answer :
                self.open_reset_password()
            else:
                QMessageBox.critical(self,"Error","Réponse secrète invalide.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {e}")
            
    def get_secret_question(self):
        try:
            self.secret_question = self.controller.get_secret_question(self.username)
            if self.secret_question:
                self.secret_question_label.set_text(self.secret_question)
                self.secret_question_label.setProperty("class","dark")
        except Exception as e:
            raise e
    
    def open_sinup(self):
        from authentication.sign_up import SignUp
        self.signup = SignUp() 
        self.signup.show()
        self.close()
    
    def open_reset_password(self):
        from authentication.password_reset import ResetPassword
        self.reset_password = ResetPassword(self.username) 
        self.reset_password.show()
        self.close()
        
    def open_login(self):
        from authentication.sign_in import SignIn
        self.signin = SignIn() 
        self.signin.show()
        self.close()
        
if __name__ == "__main__":
    app = QApplication([])

    window = PasswordForget("Borel")
    window.show()

    app.exec()
