from pathlib import Path
from pyside6_custom_widgets.dashboard import Dashboard

from imports import QTimer, Qt, QIcon, QSize, QMessageBox
from utils.utils import set_app_icon

class MainWindow(Dashboard):
    
    def __init__(self):
        super().__init__(menus=self.setup_menu(),sidebar_buttons=self.setup_sidebar())
        self.setWindowTitle("Gestionnaire de caisse") 
        set_app_icon(self)

        #self.inactivity_timer = QTimer(self)
        #self.inactivity_timer.timeout.connect(self.handle_inactivity)
        
        #self.inactivity_duration = 1 * 60 * 1000 
        #self.start_inactivity_timer()
        
        
    def setup_menu(self):
        menus = [
            ("File", [("Fermer", self.close), ("Actualiser", lambda: print("Actualisation..."))]),
            ("Révenus", [("Catégories", lambda: print("Catégorie...")), ("Nouveau Revenu", lambda: print("Ajout d'un nouveau revenu...")), ("Liste des Revenus", lambda: print("Liste Revenu..."))]),
            ("Dépenses", [("Catégories", lambda: print("Catégorie Dépenses...")), ("Nouvelle Dépense", lambda: print("Ajout d'une nouvelle dépense...")), ("Liste des Dépenses", lambda: print("Liste Dépenses..."))]),
        ]
        return menus
    
    def setup_sidebar(self):
        sidebar_buttons = [
            ("Accueil", "fa.home", lambda: print("Home...")),
            ("Paramètres", 'fa.cog', "",[("Fermer",'fa.close', self.close), ("Actualiser",'fa.star', lambda: print("Actualisation..."))]),
            ("About", 'fa.info-circle', lambda: print("Apropos...")),
            ("Déconnection", 'fa.power-off', self.open_signin)
        ]
        return sidebar_buttons
    
    # def start_inactivity_timer(self):
    #     """Démarrer ou redémarrer le timer d'inactivité."""
    #     self.inactivity_timer.start(self.inactivity_duration)

    def handle_inactivity(self):
        """Cette méthode est appelée lorsque 15 minutes d'inactivité sont atteintes."""
        print("Vous avez été déconnecté pour inactivité.")
        
        self.open_signin()

    def open_signin(self):
        """Affiche le formulaire de connexion et cache le Dashboard."""
        from authentication.sign_in import SignIn
        self.signin_form = SignIn()   
        self.signin_form.show()
        self.close()

    # def eventFilter(self, source, event):
    #     """Détecte les événements de souris et clavier pour réinitialiser le timer."""
    #     if event.type() in [Qt.MouseMove, Qt.KeyPress]:
    #         self.start_inactivity_timer()
    #     return super().eventFilter(source, event)
    
if __name__ == "__main__":
    import sys
    from imports import QApplication
    app = QApplication([])
    win = MainWindow()
    win.show()
    
    sys.exit(app.exec())