from imports import  QPushButton,  QSize, QHBoxLayout, QWidget
import qtawesome as qta
from pyside6_custom_widgets.line_edit import LineEdit

class SearchBar(QWidget):
    """
    Custom search bar widget with a LineEdit and a search button.
    """

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)

        self.search_input = LineEdit(placeholder_text='Search')
        self.search_button = QPushButton(qta.icon("fa.search"), "")
        self.search_button.setFixedSize(QSize(40, 40))

        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)

        self.setLayout(layout)

    def connect_search_button(self, slot):
        """
        Connects the search button's clicked signal to a slot.

        Args:
            slot (callable): The function to call when the search button is clicked.
        """
        self.search_button.clicked.connect(slot)

    def get_search_text(self):
        """
        Returns the text entered in the search input.

        Returns:
            str: The search text.
        """
        return self.search_input.text()
