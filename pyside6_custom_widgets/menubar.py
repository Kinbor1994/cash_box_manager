from imports import QMenuBar, QPushButton, QAction, QSize, Qt

import qtawesome as qta

from utils.qss_file_loader import load_stylesheet


class MenuBar(QMenuBar):
    """
    Custom MenuBar with a pushMenu button and dynamic addition of menu items.
    """

    def __init__(self, menus=[], push_menu_button=True):
        """
        Initializes the MenuBar with optional menus and a pushMenu button.

        Args:
            menus (list of tuples): A list of tuples where each tuple represents
                                a menu and its actions.
                                Example: [("File", [("New", new_func), ("Open", open_func)]), ...]
            push_menu_button (bool): Whether to include the pushMenu button. Defaults to True.
        """
        super().__init__()

        # Optionally add a pushMenu button
        if push_menu_button:
            self.push_menu_button = QPushButton(qta.icon("fa.bars"), "")
            self.push_menu_button.setFixedSize(QSize(40, 40))
            self.setCornerWidget(self.push_menu_button, Qt.TopLeftCorner)

        self.setStyleSheet(load_stylesheet("styles/menu_bar.qss"))
        # Add custom menus
        self.add_menus(menus)

    def add_menus(self, menus):
        """
        Adds menus and their actions to the MenuBar.

        Args:
            menus (list of tuples): A list of tuples where each tuple represents
                                a menu and its actions.
        """
        for menu_name, actions in menus:
            menu = self.addMenu(menu_name)
            for action_name, action_func in actions:
                action = QAction(action_name, self)
                action.triggered.connect(action_func)
                menu.addAction(action)

    def connect_push_menu(self, slot):
        """
        Connects the pushMenu button to a slot/function.

        Args:
            slot (callable): The function to call when the pushMenu button is clicked.
        """
        if hasattr(self, "push_menu_button"):
            self.push_menu_button.clicked.connect(slot)





if __name__ == "__main__":
    from imports import QApplication, QMainWindow, QVBoxLayout, QWidget
    import sys
    
    def new_file():
        print("New file created!")

    def open_file():
        print("File opened!")

    def toggle_sidebar():
        print("Sidebar toggled!")
        
    app = QApplication([])

    window = QMainWindow()
    layout = QVBoxLayout()

    # Define the menus with their corresponding actions
    menus = [
        ("File", [("New", new_file), ("Open", open_file)]),
        ("Edit", [("Undo", lambda: print("Undo")), ("Redo", lambda: print("Redo"))]),
    ]

    # Create the MenuBar with custom menus and a pushMenu button
    menubar = MenuBar(menus=menus)
    menubar.connect_push_menu(toggle_sidebar)
    window.setMenuBar(menubar)

    central_widget = QWidget()
    central_widget.setLayout(layout)
    window.setCentralWidget(central_widget)

    window.resize(800, 600)
    window.show()

    sys.exit(app.exec())