from imports import QWidget, QHBoxLayout, QPushButton, QLineEdit 

class HeaderWidget(QWidget):
    """
    Header widget containing a "Home" button and a search bar.

    Args:
        parent (QWidget, optional): The parent widget. Defaults to None.
    """

    def __init__(self):
        super().__init__()
        self.setup_header()

    def setup_header(self):
        """
        Sets up the header widget.
        """
        self.setFixedHeight(60)

        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)

        self.home_button = QPushButton("Home")  
        layout.addWidget(self.home_button)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")  
        layout.addWidget(self.search_bar)

        self.setLayout(layout)

    def get_widget(self):
        """
        Returns the main widget (self).

        Returns:
            QWidget: The main widget.
        """
        return self