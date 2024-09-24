from controllers.user_controller import UserController
from database.create_db import check_and_create_db
from pyside6_custom_widgets.signin import SignIn
from main import MainWindow
from imports import QSize, QMessageBox
from utils.utils import set_app_icon

class SignIn(SignIn):
    
    def __init__(self):
        super().__init__()
        self.setGeometry(100,100,350, 220)
        self.setMinimumSize(QSize(350, 220))
        self.setMaximumSize(QSize(350, 220))
        set_app_icon(self)
        self.controller = UserController()
        self.setup_connection()
        
    def setup_connection(self):
        self.connect_button.clicked.connect(self.login)
        
    def login(self):
        try:
            if self.validate_fields():
                username, password = self.get_credentials()
                is_authenticated = self.controller.authenticate_user(username,password)
                if is_authenticated :
                    # QMessageBox.information(self,"Success","Connection approuvée")
                    self.open_dashboard()
                else:
                    QMessageBox.critical(self,"Error","Nom d'utilisateur ou Mot de passe incorrecte.")
            else:
                QMessageBox.critical(self, "Error", "Vous devrez renseigner tous les champs.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {e}")
    
    def open_dashboard(self):
        self.dashboard = MainWindow()  
        self.dashboard.show()
        self.close()  
        
    def showEvent(self,event):
        super().showEvent(event)
        check_and_create_db()
        
if __name__ == "__main__":
    import sys
    from imports import QApplication
    app = QApplication([])
    
    win = SignIn()
    win.show()
    
    sys.exit(app.exec())