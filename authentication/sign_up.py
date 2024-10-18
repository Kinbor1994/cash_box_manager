from pathlib import Path
from controllers.user_controller import UserController
from database.create_db import check_and_create_db
from imports import QDialog, QVBoxLayout, QHBoxLayout, QIcon, QSize, QMessageBox, QFrame
from pyside6_custom_widgets.labeled_combobox_2 import LabeledComboBox
from pyside6_custom_widgets.combobox_2 import ComboBox
from pyside6_custom_widgets.labeled_line_edit import LabeledLineEdit
from pyside6_custom_widgets.button import Button
from pyside6_custom_widgets.line_edit import LineEdit
from authentication.sign_in import SignIn
from utils.utils import secret_questions, set_app_icon

from qt_material import apply_stylesheet

class SignUp(QDialog):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CASH BOX MANAGER BY BOREL")
        set_app_icon(self)
        self.setGeometry(100,100,500, 480)
        self.setMinimumSize(QSize(500, 480))
        self.setMaximumSize(QSize(500, 480))
        self.controller = UserController()
        
        self.setup_ui()
        self.setup_connections()
        
        apply_stylesheet(self, theme="default_light.xml")
        
    def setup_ui(self):
        self.main_layout = QVBoxLayout()
        self.btn_layout = QHBoxLayout()
        self.password_layout = QHBoxLayout()
        self.username_widget = LabeledLineEdit(label_text="Identifiant",placeholder_text="Saisissez votre identifiant...",error_message="Ce champ est obligatoire",required=True)
        self.password_widget = LabeledLineEdit(label_text="Mot de passe",placeholder_text="Saisissez votre mot de passe...",error_message="Ce champ est obligatoire", input_type="password", required=True)
        self.confirm_password_widget = LabeledLineEdit(label_text="Confirmer le mot de passe",placeholder_text="Confirmez votre mot de passe...",error_message="Ce champ est obligatoire", input_type="password", required=True)
        self.secret_question_widget = LabeledComboBox(items=secret_questions,label_text="Question", placeholder="Sélectionnez une question...", required=True)
        self.secret_answer_widget = LabeledLineEdit(label_text="Réponse",placeholder_text="Saisissez votre réponse...",error_message="Ce champ est obligatoire",required=True)
        self.submit_btn = Button(text="S'inscrire",icon_name="fa.sign-in",theme_color="primary")
        self.cancel_btn = Button(text="Fermer",icon_name="fa.sign-out",theme_color="danger")
        self.password_layout.addWidget(self.password_widget)
        self.password_layout.addWidget(self.confirm_password_widget)
        
        #Separator
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        
        self.signin_button = Button(text="Vous avez déjà un compte compte ? Connectez-vous ici...",theme_color="info")
        
        self.main_layout.addWidget(self.username_widget)
        self.main_layout.addLayout(self.password_layout)
        self.main_layout.addWidget(self.secret_question_widget)
        self.main_layout.addWidget(self.secret_answer_widget)
        self.btn_layout.addWidget(self.submit_btn)
        self.btn_layout.addWidget(self.cancel_btn)
        self.main_layout.addLayout(self.btn_layout)
        self.main_layout.addWidget(self.separator)
        self.main_layout.addWidget(self.signin_button)
        self.setLayout(self.main_layout)
        
    def setup_connections(self):
        self.submit_btn.clicked.connect(self.on_submit)
        self.signin_button.clicked.connect(self.open_signin)
        self.cancel_btn.clicked.connect(self.close)
        
    def validate_fields(self):
        """
        Validates the fields and highlights any empty fields with a red border.
        """
        fields = [
            self.username_widget.line_edit,
            self.password_widget.line_edit,
            self.confirm_password_widget.line_edit,
            self.secret_answer_widget.line_edit,
            self.secret_question_widget.combobox
        ]
        all_valid = True
        
        for field in fields:
            if isinstance(field, LineEdit):
                if not field.is_valid():
                    field.line_edit.setStyleSheet("border: 2px solid red;")
                    all_valid = False
                else:
                    field.line_edit.setStyleSheet("")  
            elif isinstance(field, ComboBox):
                if not field.is_valid():  
                    field.combobox.setStyleSheet("border: 2px solid red;")
                    all_valid = False
                else:
                    field.combobox.setStyleSheet("")  
        
        if self.password_widget.line_edit.get_text() == self.confirm_password_widget.line_edit.get_text():
            self.password_widget.line_edit.setStyleSheet("")
            self.confirm_password_widget.line_edit.setStyleSheet("") 
        else:
            self.password_widget.line_edit.setStyleSheet("border: 2px solid red;")
            self.confirm_password_widget.line_edit.setStyleSheet("border: 2px solid red;")
            all_valid = False
            QMessageBox.warning(self, "Error", "Les mot de passes doivent être conforme.")
            
        return all_valid
    
    def get_credentials(self):
        """
        Returns the entered username, password, secret_question and secret_answer if the input is valid.

        Returns:
            tuple: A tuple containing the username, password, secret_question and secret_answer if valid, otherwise (None, None, None, None).
        """
        if self.validate_fields():
            return self.username_widget.get_text(), self.password_widget.get_text(), self.secret_question_widget.get_selected_text(), self.secret_answer_widget.get_text()
        else:
            return None, None, None, None
        
    def create_user(self):
        try:
            username, password, secret_question, secret_answer = self.get_credentials()
            if username and password and secret_question and secret_answer:
                user = self.controller.create_user(username, password, secret_question, secret_answer)
                if user:
                    self.open_signin()
            else:
                QMessageBox.critical(self, "Error", "Veuillez remplir tous les champs correctement.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {e}")
    
    def on_submit(self):
        if self.validate_fields():
            self.create_user()
        else:
            QMessageBox.critical(self, "Error", "Vous devrez renseigner tous les champs correctement.")
            
    def open_signin(self):
        self.signin = SignIn()  
        self.signin.show()
        self.close()  
        
    def showEvent(self,event):
        super().showEvent(event)
        check_and_create_db()
        
if __name__ == "__main__":
    import sys
    from imports import QApplication
    app = QApplication([])
    
    win = SignUp()
    win.show()
    
    sys.exit(app.exec())