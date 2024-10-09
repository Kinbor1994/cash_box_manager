import sys

from imports import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QLabel, Qt
)

import qtawesome as qta
from qt_material import apply_stylesheet
from pyside6_custom_widgets import MenuBar
from pyside6_custom_widgets import SearchBar
from pyside6_custom_widgets import SideBar
from pyside6_custom_widgets import Content
from utils.qss_file_loader import load_stylesheet


class Dashboard(QMainWindow):
    """
    Main Dashboard class that manages the overall layout and components. It provides a flexible
    framework for building a dashboard interface with a menu bar, sidebar, content area, and
    search bar, while offering styling via QSS or Qt Material themes.

    Attributes:
        menus (list): List of menu items for the MenuBar.
        sidebar_buttons (list): List of buttons for the SideBar.
        style (str): QSS style for the dashboard, default is loaded from a file.
        use_qt_material (bool): Flag to use Qt Material theme instead of QSS.
        menu_bar (MenuBar): The top menu bar for navigation.
        search_bar (SearchBar): Search bar placed in the top-right corner of the menu.
        side_bar (SideBar): Sidebar with navigation buttons.
        content (Content): Central content area where pages are displayed.
    """

    def __init__(self, menus=None, sidebar_buttons=None, style_or_theme="", use_qt_material=False):
        """
        Initializes the Dashboard layout, including the MenuBar, SideBar, Content area, and SearchBar.

        Args:
            menus (list, optional): List of menu tuples for the MenuBar. Defaults to None.
            sidebar_buttons (list, optional): List of sidebar button tuples. Defaults to None.
            style_or_theme (str, optional): Custom QSS style for the dashboard. Or the theme if uses Qt Materiel. Defaults to "".
            use_qt_material (bool, optional): Flag to use Qt Material theme. Defaults to False.
        """
        super().__init__()
        self.setWindowTitle("My Dashboard")
        self.setGeometry(100, 100, 1000, 600)
        self.use_qt_material = use_qt_material

        # Ensure menus and sidebar_buttons are not mutable defaults
        self.menus = menus or []
        self.sidebar_buttons = sidebar_buttons or []

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create and add MenuBar, SearchBar, SideBar, and Content
        self.menu_bar = MenuBar(menus=self.menus)
        self.search_bar = SearchBar()
        self.menu_bar.setCornerWidget(self.search_bar, Qt.TopRightCorner)

        self.side_bar = SideBar(buttons=self.sidebar_buttons)
        self.content = Content()

        main_layout.addWidget(self.side_bar)
        main_layout.addWidget(self.content)
        self.setMenuBar(self.menu_bar)

        # Connect pushMenu button to toggle sidebar
        self.menu_bar.connect_push_menu(self.side_bar.toggle_sidebar)
        
        # Apply the appropriate style (QSS or Material)
        self.set_style(style_or_theme)

    def add_content_page(self, page_widget, title):
        """
        Adds a new page to the content area.

        Args:
            page_widget (QWidget): The widget representing the page to add.
            title (str): The title of the page.
        """
        self.content.add_page(page_widget, title)
        
    def set_current_page_by_index(self, index):
        self.content.set_current_page_by_index(index)
        
    def set_current_page(self, page_widget):
        self.content.set_current_page(page_widget)
        
    def set_style(self, style_or_theme):
        """
        Applies the QSS style or clears the styles for Qt Material usage.

        Args:
            style_or_theme (str): Custom QSS style for the dashboard.
        """
        if self.use_qt_material:
            self.apply_material_style(style_or_theme)  # Clears the QSS when using Qt Material theme
        else:
            self.apply_qss_style(style_or_theme)

    def apply_qss_style(self, style):
        """
        Applies the QSS stylesheet to the dashboard.

        Args:
            style (str): Path to the QSS file or inline QSS string.
        """
        if style:
            self.setStyleSheet(style)  # Apply the provided style string
        else:
            try:
                # Load the default QSS style from file
                self.setStyleSheet(load_stylesheet("styles/dashboard.qss"))
            except FileNotFoundError as e:
                print(f"Error loading stylesheet: {e}")
                # Apply a fallback style
                self.setStyleSheet("background-color: #f0f0f0;")

    def apply_material_style(self, theme):
        """
        Applies the Qt Material theme. Clears the QSS stylesheet.
        
        Args:
            style_or_theme (str): The Qt Material Theme.
        """
        self.setStyleSheet("")  # Clear any QSS when using Qt Material
        # Logic to apply the Qt Material theme would go here
        if theme:
            apply_stylesheet(self, theme=theme)
        else:
            apply_stylesheet(self, theme="dark_teal.xml")

        


if __name__ == "__main__":
    from imports import QApplication, QLabel
    import sys
    import qtawesome as qta

    def new_file():
        print("New file created!")

    def open_file():
        print("File opened!")

    def home_action():
        print("Home button clicked!")

    def settings_action():
        print("Settings button clicked!")

    def about_action():
        print("About button clicked!")

    app = QApplication([])

    # Define the menus with their corresponding actions
    menus = [
        ("File", [("New", new_file), ("Open", open_file)]),
        ("Edit", [("Undo", lambda: print("Undo")), ("Redo", lambda: print("Redo"))]),
    ]

    def main_action():
        print("Main action triggered!")

    def bonjour():
        dashboard.content.stacked_widget.setCurrentIndex(2)
        
    def sub_action_1():
        print("Sub action 1 triggered!")

    def sub_action_2():
        print("Sub action 2 triggered!")
    # Define the sidebar buttons with their corresponding actions
    sidebar_buttons = [
        ("Home", "fa.home", main_action, [("Sub1", 'fa.star', sub_action_1), ("Sub2", 'fa.heart', sub_action_2)]),
        ("Settings", 'fa.cog', bonjour,[("Sub1", 'fa.star', sub_action_1), ("Sub2", 'fa.heart', sub_action_2)]),
        ("About", 'fa.info-circle', main_action,[("Sub1", 'fa.star', sub_action_1), ("Sub2", 'fa.heart', sub_action_2)])
    ]


    # Create the Dashboard
    dashboard = Dashboard(menus=menus, sidebar_buttons=sidebar_buttons)

    # Add some content pages
    page1 = QLabel("This is Page 1")
    page2 = QLabel("This is Page 2")
    page3 = QLabel("This is Page 3")

    dashboard.add_content_page(page1, "Title 1")
    dashboard.add_content_page(page2, "Title 2")
    dashboard.add_content_page(page3, "Title 3")

    dashboard.show()

    sys.exit(app.exec())