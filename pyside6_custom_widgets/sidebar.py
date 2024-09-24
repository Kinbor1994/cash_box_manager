from imports import QWidget, QVBoxLayout, QPushButton, QSize, Qt, QFrame

import qtawesome as qta

from utils.qss_file_loader import load_stylesheet

class SideBar(QWidget):
    """
    Manages the two sidebars (compact and full) and toggling between them.
    Allows dynamic addition of buttons with associated commands and sub-buttons.
    """

    def __init__(self, buttons):
        """
        Initializes the SideBar with a list of buttons.

        Args:
            buttons (list of tuples): A list of tuples where each tuple contains
                                the button text, the icon name, the function to connect,
                                and optionally a list of sub-buttons.
                                Example: [("Home", 'fa.home', some_function, [("Sub1", "fa.heart", sub1_func), ...]), ...]
        """
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.active_button = None
        # Create compact and full sidebars
        self.compact_sidebar = self.create_sidebar(compact=True, buttons=buttons)
        self.full_sidebar = self.create_sidebar(compact=False, buttons=buttons)

        # Initially show the full sidebar
        self.layout.addWidget(self.compact_sidebar)
        self.layout.addWidget(self.full_sidebar)
        self.compact_sidebar.hide()
        self.setStyleSheet(load_stylesheet("styles/side_bar.qss"))

    def create_sidebar(self, compact=False, buttons=[]):
        """
        Creates a sidebar with buttons and optional text labels.

        Args:
            compact (bool): Whether to create the compact version (icons only).
            buttons (list of tuples): A list of tuples where each tuple contains
                                the button text, the icon name, the function to connect,
                                and optionally a list of sub-buttons.

        Returns:
            QWidget: The configured sidebar widget.
        """
        sidebar = QWidget()
        layout = QVBoxLayout(sidebar)
        layout.setAlignment(Qt.AlignTop)

        # Add buttons to the sidebar
        for button_data in buttons:
            text, icon_name, command = button_data[:3]
            sub_buttons = button_data[3] if len(button_data) > 3 else []

            # Create the main button
            if icon_name:
                button = QPushButton(qta.icon(icon_name), text if not compact else "")
            else:
                button = QPushButton(text if not compact else "")
            button.setIconSize(QSize(24, 24))
            if command:
                button.clicked.connect(command)
            button.clicked.connect(lambda _, b=button: self.set_active_button(b))
            
            # Create a frame to hold sub-buttons
            sub_button_frame = QFrame()
            sub_button_layout = QVBoxLayout(sub_button_frame)
            sub_button_layout.setContentsMargins(30, 0, 0, 0)  # Indent sub-buttons
            sub_button_frame.hide()  # Hide sub-buttons by default

            # Add sub-buttons if any
            for sub_text, sub_icon_name, sub_command in sub_buttons:
                if sub_icon_name:
                    sub_button = QPushButton(qta.icon(sub_icon_name), sub_text if not compact else "")
                else:
                    sub_button = QPushButton(sub_text if not compact else "")
                sub_button.setIconSize(QSize(20, 20))
                sub_button.clicked.connect(sub_command)
                sub_button.clicked.connect(lambda _, sb=sub_button: self.set_active_button(sb))
                sub_button_layout.addWidget(sub_button)

            # Toggle visibility of sub-buttons on main button click
            button.clicked.connect(lambda _, f=sub_button_frame: f.setVisible(not f.isVisible()))
            
            layout.addWidget(button)
            layout.addWidget(sub_button_frame)

        # Set fixed width based on compact/full mode
        sidebar.setFixedWidth(80 if compact else 200)
        return sidebar

    def set_active_button(self, button):
        """
        Manages the active state of both main buttons and sub-buttons.
        Applies the active style to the clicked button and removes it from others.
        """
        if self.active_button:
            self.active_button.setStyleSheet("")  
        
        button.setStyleSheet("background-color: #1abc9c; color: white; font-weight: bold;")
        
        self.active_button = button
        
    def toggle_sidebar(self):
        """
        Toggles between compact and full sidebar views.
        """
        self.full_sidebar.setVisible(not self.full_sidebar.isVisible())
        self.compact_sidebar.setVisible(not self.compact_sidebar.isVisible())

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
    import sys

    def main_action():
        print("Main action triggered!")

    def bonjour():
        print("Hello!")
        
    def sub_action_1():
        print("Sub action 1 triggered!")

    def sub_action_2():
        print("Sub action 2 triggered!")

    app = QApplication([])

    # Define the sidebar buttons with their corresponding actions and sub-buttons
    sidebar_buttons = [
        ("Home", None, main_action, [("Sub1", 'fa.star', sub_action_1), ("Sub2", 'fa.heart', sub_action_2)]),
        ("Settings", 'fa.cog', bonjour,[("Sub1", 'fa.star', sub_action_1), ("Sub2", 'fa.heart', sub_action_2)]),
        ("About", 'fa.info-circle', main_action,[("Sub1", 'fa.star', sub_action_1), ("Sub2", 'fa.heart', sub_action_2)])
    ]

    # Create the SideBar
    sidebar = SideBar(buttons=sidebar_buttons)

    # Set up the main window
    window = QMainWindow()
    layout = QVBoxLayout()
    layout.addWidget(sidebar)

    central_widget = QWidget()
    central_widget.setLayout(layout)
    window.setCentralWidget(central_widget)

    window.resize(300, 600)
    window.show()

    sys.exit(app.exec())