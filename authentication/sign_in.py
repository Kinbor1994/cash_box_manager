from pathlib import Path
from controllers.cash_box_controller import CashBoxPeriodController
from controllers.user_controller import UserController
from database.create_db import check_and_create_db
from pyside6_custom_widgets.button import Button
from pyside6_custom_widgets.labeled_line_edit import LabeledLineEdit
from pyside6_custom_widgets.labeled_combobox_2 import LabeledComboBox
from pyside6_custom_widgets.label import Label
from imports import QDialog, QVBoxLayout, QHBoxLayout,QIcon, QLineEdit, QApplication,QSize, QMessageBox, QFrame
from qt_material import apply_stylesheet

from main import MainWindow
from utils.utils import save_config_data, set_app_icon, write_id_to_file
from views.manage_periodes_views import CashBoxPeriodCreateView

class SignIn(QDialog):
    """
    A dialog for user sign-in with username and password fields.

    Args:
        parent (QWidget, optional): The parent widget. Defaults to None.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("CASH BOX MANAGER BY BOREL")
        set_app_icon(self)
        self.setGeometry(100,100,400, 400)
        self.setMinimumSize(QSize(400, 400))
        self.setMaximumSize(QSize(400, 400))
        self.is_any_period_created() # Vérifier s'il existe des exercices sinon en créer d'abord.
        self.controller = UserController()
        self.setup_ui()
        self.setup_connection()
        apply_stylesheet(self, theme="default_light.xml")

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
        
        #Current Period field
        periodes = CashBoxPeriodController().get_all()
        items = []
        for period in periodes:
            data = {}
            data["id"] = period.id
            data["label"] = f"{period.start_date.strftime("%d/%m/%Y")} - {period.end_date.strftime("%d/%m/%Y")}"
            items.append(data)
            
        self.period_cbx = LabeledComboBox(label_text="Selectionnez un exercice...", required=True, items=items)
        layout.addWidget(self.period_cbx)
        # Buttons
        button_layout = QHBoxLayout()
        self.connect_button = Button(text="Connect",icon_name="fa.sign-in",theme_color="primary")
        self.cancel_button = Button(text="Cancel",icon_name="fa.sign-out",theme_color="danger")
        
        button_layout.addWidget(self.connect_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        #Separator
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(self.separator)
        
        #Signup or reset password button
        self.password_forget_button = Button(text="Mot de passe oublié ?",theme_color="info")
        self.signup_button = Button(text="Pas encore de compte ? Créez un compte...",theme_color="warning")
        self.infos_label = Label(text="Ou")
        layout.addWidget(self.password_forget_button)
        layout.addWidget(self.infos_label)
        layout.addWidget(self.signup_button)
        self.setLayout(layout)
        layout.addStretch(1)
    
    
    def setup_connection(self):
        self.connect_button.clicked.connect(self.on_submit)
        self.cancel_button.clicked.connect(self.close)
        self.signup_button.clicked.connect(self.open_sinup)
        self.password_forget_button.clicked.connect(self.open_password_forget)
        
    def validate_fields(self):
        """
        Validates the fields and highlights any empty fields with a red border.
        """
        fields = [self.username_field, self.password_field, self.period_cbx]
        all_valid = []

        for field in fields:
            all_valid.append(field.is_valid())

        return all(all_valid)

    def get_credentials(self):
        """
        Returns the entered username and password if the input is valid.

        Returns:
            tuple: A tuple containing the username and password if valid, otherwise (None, None).
        """
        if self.validate_fields():
            return self.username_field.get_value(), self.password_field.get_value(), self.period_cbx.get_value()
        else:
            return None, None, None

    def on_submit(self):
        if self.validate_fields():
            self.login()
        else:
            QMessageBox.critical(self, "Error", "Vous devrez renseigner tous les champs.")
            
    def login(self):
        try:
            username, password, period_id = self.get_credentials()
            is_authenticated = self.controller.authenticate_user(username,password)
            if is_authenticated :
                user = self.controller.get_user(username=username)
                save_config_data(user[0], user[1]) #Enregistrer les données de l'utilisateur connecté.
                write_id_to_file(str(period_id)) #Enregistrer l'id de l'exercice choisit
                self.open_dashboard()
            else:
                QMessageBox.critical(self,"Error","Nom d'utilisateur ou Mot de passe incorrecte.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {e}")
            
    def open_dashboard(self):
        self.dashboard = MainWindow()  
        self.dashboard.show()
        self.close()  
        
    def open_sinup(self):
        from authentication.sign_up import SignUp
        self.signup = SignUp() 
        self.signup.show()
        self.close()
        
    def open_password_forget(self):
        from authentication.password_forget import PasswordForget
        self.username = self.username_field.get_text()
        if not self.username:
            QMessageBox.warning(self, "Nom d'utilisateur requis.", "Vous devez d'abord entrer votre identifiant.")
        else:
            self.password_forget = PasswordForget(self.username_field.get_text()) 
            self.password_forget.show()
            self.close()

    def is_any_period_created(self):
        periodes = CashBoxPeriodController().get_all()
        
        if not periodes:
            form = CashBoxPeriodCreateView()
            form.exec()
    
    def showEvent(self,event):
        super().showEvent(event)
        check_and_create_db()
        
if __name__ == "__main__":
    app = QApplication([])

    window = SignIn()
    window.show()

    app.exec()
