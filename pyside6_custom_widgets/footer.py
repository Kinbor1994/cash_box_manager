from imports import QWidget, QHBoxLayout, Qt
from pyside6_custom_widgets.label import Label
from utils.qss_file_loader import load_stylesheet

class Footer(QWidget):
    """
    Custom Footer widget for the Dashboard. This widget can display useful information
    or navigation links at the bottom of the application.
    """

    def __init__(self, text="Footer Text", parent=None):
        super().__init__(parent)
        self.setup_ui(text)

        self.setStyleSheet(load_stylesheet("styles/footer.qss"))
            
    def setup_ui(self, text):
        """
        Initializes the footer layout and design.

        Args:
            text (str): The text to display in the footer.
        """
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        label = Label(text, theme_name="light")
        label.setFixedHeight(35)
        label.setAlignment(Qt.AlignCenter)

        layout.addWidget(label)
