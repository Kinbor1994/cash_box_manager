import qtawesome as qta

from imports import QPushButton, QSize, QIcon, Qt
from qt_material import apply_stylesheet

from utils.qss_file_loader import load_stylesheet

class Button(QPushButton):
    """
    Custom button with text, optional icon (local or QtAwesome), and optional theme color.

    Args:
        text (str): The button text.
        icon_path (str, optional): Path to the local icon. Defaults to None.
        icon_name (str, optional): Name of the QtAwesome icon (e.g., 'fa5s.home'). Defaults to None.
        theme_color (str, optional): Theme color for styling (e.g., 'primary', 'danger'). Defaults to "primary".
        command (callable): The function to call when the button is clicked.
    """

    def __init__(self, text, icon_path=None, icon_name=None, theme_color="primary", command = None):
        super().__init__()
        self.command = command
        self.setup_button(text, icon_path, icon_name)
        self.setStyleSheet(load_stylesheet("styles/button.qss"))

        self.setProperty("class", theme_color)
        self.setCursor(Qt.PointingHandCursor)

        
    def setup_button(self, text, icon_path, icon_name):
        """
        Sets up the button with text and optional icon.

        Args:
            text (str): The button text.
            icon_path (str, optional): Path to the local icon. Defaults to None.
            icon_name (str, optional): Name of the QtAwesome icon. Defaults to None.
        """
        self.setText(text)

        if icon_path:
            icon = QIcon(icon_path)
            self.setIcon(icon)
            self.setIconSize(QSize(24, 24))
        elif icon_name:
            # Use QtAwesome to set the icon
            icon = qta.icon(icon_name)
            self.setIcon(icon)
            self.setIconSize(QSize(24, 24)) 
            
        self.connect_clicked()
    
    def connect_clicked(self):
        """
        Connects the button's clicked signal to a slot.
        """
        self.clicked.connect(self.command)

    def get_widget(self):
        """
        Returns the main widget (self).

        Returns:
            QPushButton: The button widget.
        """
        return self