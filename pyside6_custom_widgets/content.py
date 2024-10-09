from imports import QWidget, QVBoxLayout, QStackedWidget, QHBoxLayout, QLabel
from utils.qss_file_loader import load_stylesheet

class Content(QWidget):
    """
    Manages the central content area using a QStackedWidget.
    Each page added will include a title above it in a layout of fixed width.
    """

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        # Create stacked widget to hold content pages
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

    def add_page(self, page_widget, title):
        """
        Adds a new page to the stacked widget with a title above it.

        Args:
            page_widget (QWidget): The widget to add as a new page.
            title (str): The title of the page, displayed above the content.
        """
        # Create a wrapper widget to hold the title and the page content
        page_wrapper = QWidget()
        page_layout = QVBoxLayout(page_wrapper)
        page_layout.setContentsMargins(5, 5, 5, 5)  # No margins around the layout

        # Create the title label with a fixed width of 45 pixels
        title_label = QLabel(title)
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_label.setProperty("role","title")
        title_label.setStyleSheet(load_stylesheet("styles/label.qss"))
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        title_label.setFixedHeight(45)

        # Add the title layout and page content to the page layout
        page_layout.addLayout(title_layout)
        page_layout.addWidget(page_widget)

        # Add the wrapped page (with title) to the stacked widget
        self.stacked_widget.addWidget(page_wrapper)

    def set_current_page_by_index(self, index):
        """
        Sets the current page to the specified index.

        Args:
            index (int): The index of the page to display.
        """
        self.stacked_widget.setCurrentIndex(index)
    
    def set_current_page(self, page_widget):
        """
        Sets the current.

        Args:
            index (QWidget): The widget of the page to display.
        """
        self.stacked_widget.setCurrentWidget(page_widget)



if __name__ == "__main__":
    from imports import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
    import sys
    
    app = QApplication([])

    window = QMainWindow()
    layout = QVBoxLayout()

    # Create the content area
    content_area = Content()

    # Add some example pages
    page1 = QLabel("This is Page 1")
    page2 = QLabel("This is Page 2")
    page3 = QLabel("This is Page 3")

    content_area.add_page(page1, "Title 1")
    content_area.add_page(page2, "Title 2")
    content_area.add_page(page3, "Title 3")

    # Create buttons to navigate between pages
    button_layout = QHBoxLayout()
    
    button1 = QPushButton("Show Page 1")
    button1.clicked.connect(lambda: content_area.set_current_page(0))
    button_layout.addWidget(button1)

    button2 = QPushButton("Show Page 2")
    button2.clicked.connect(lambda: content_area.set_current_page(1))
    button_layout.addWidget(button2)

    button3 = QPushButton("Show Page 3")
    button3.clicked.connect(lambda: content_area.set_current_page(2))
    button_layout.addWidget(button3)

    layout.addLayout(button_layout)
    layout.addWidget(content_area)

    central_widget = QWidget()
    central_widget.setLayout(layout)
    window.setCentralWidget(central_widget)

    window.resize(800, 600)
    window.show()

    sys.exit(app.exec())