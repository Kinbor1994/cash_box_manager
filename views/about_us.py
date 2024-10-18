from imports import QDialog, QHBoxLayout, QVBoxLayout, Qt
from pyside6_custom_widgets.button import Button
from pyside6_custom_widgets.label import Label
from utils.utils import set_app_icon
from qt_material import apply_stylesheet
class AboutUs(QDialog):
    
    content = """
        Version: 1.0.0
        Année de sortie: 2024
        
        Author: KINNOUME S. Borel
        ☎️Contact: +22966852350  
        📧Email: kinnoumeb@gmail.com
        
        Description: CASH BOX MANAGER  
        Est un logiciel de gestion de caisse.
        Il vous permet de suivre vos recettes 
        et dépenses et intègre quelques 
        petites options d'analyse rapide.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CASH BOX MANAGER BY BOREL")
        self.setFixedSize(400,300)
        set_app_icon(self)
        apply_stylesheet(self, theme="default_light.xml")
        self.setup_ui()
        
    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10,5,10,5)
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(0,0,0,0)
        title_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(25,0,0,0)
        content_layout.setAlignment(Qt.AlignLeft| Qt.AlignCenter)
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0,0,0,0)
        btn_layout.setAlignment(Qt.AlignRight | Qt.AlignTop)
        
        title_label = Label(text="CASH BOX MANAGER BY BOREL", theme_name="primary", icon_color="blue")
        icon_label = Label(text="",icon_name="fa.info-circle", theme_name="primary", icon_color="blue")
        icon_label.setFixedSize(50, 50)
        title_layout.addWidget(icon_label)
        title_layout.addWidget(title_label)
        
        content_label = Label(text=self.content)
        content_label.set_property("class","content")
        content_layout.addWidget(content_label)
        
        close_btn = Button(text="Fermer", icon_name="fa.close", theme_color="danger")
        close_btn.clicked.connect(self.close)
        btn_layout.addWidget(close_btn)
        
        main_layout.addLayout(title_layout)
        main_layout.addLayout(content_layout)
        main_layout.addLayout(btn_layout)
        main_layout.addStretch()
        self.setLayout(main_layout)
        
        
if __name__ == "__main__":
    import sys
    from imports import QApplication
    
    app = QApplication([])
    win = AboutUs()
    win.show()
    sys.exit(app.exec())