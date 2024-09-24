import qtawesome as qta
from imports import QComboBox, QEvent, QWidget, QLabel, QVBoxLayout

from utils.qss_file_loader import load_stylesheet

class ComboBox(QWidget):
    """
    A custom widget for QComboBox with built-in validation, error display, and customizable styles.

    Args:
        items_with_data (list): A list of tuples, where each tuple contains (item, userData). Default to [].
            Example: [("Item 1", 1), ("Item 2", 2), ...]
        required (bool, optional): Whether the selection is required. Defaults to False.
        validation_func (callable, optional): A custom validation function. Defaults to None.
        error_message (str, optional): Custom error message to display when validation fails. Defaults to "Please select an option".
        custom_style (str, optional): Custom QSS style to apply to the widget. If not provided, defaults to "combobox.qss".
        on_selection_changed_func (callable, optional): Function triggered when the selection changes in the QComboBox.
        parent (QWidget, optional): The parent widget. Defaults to None.
    """

    def __init__(self, items_with_data=[], placeholder="Select an option........", required=False, validation_func=None, error_message="Please select an option", 
        custom_style=None, on_selection_changed_func=None, parent=None):
        super().__init__(parent)
        self.required = required
        self.placeholder = placeholder 
        self.validation_func = validation_func
        self.error_message = error_message
        self.on_selection_changed_func = on_selection_changed_func
        self.error_label = QLabel()

        self.setup_widget(items_with_data)

        # Set custom style if provided, otherwise load default style
        if custom_style:
            self.setStyleSheet(custom_style)
        else:
            self.setStyleSheet(load_stylesheet("styles/combobox.qss"))

    def setup_widget(self, items_with_data):
        """
        Sets up the QComboBox widget with optional items.
        """
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Create QComboBox
        self.combobox = QComboBox()
        self.set_items(items_with_data)

        self.combobox.currentIndexChanged.connect(self.on_current_index_changed)
        # Connect the signal for selection change to the custom method
        self.combobox.currentIndexChanged.connect(self.on_selection_changed)

        # Install event filter to capture focus events
        self.combobox.installEventFilter(self)
        
        # Add combo box and error label to the layout
        layout.addWidget(self.combobox)
        layout.addWidget(self.error_label)
        self.error_label.setStyleSheet("color: red;")  # Default error message style
        self.error_label.hide()

        self.setLayout(layout)

    def set_items(self, items_with_data):
        """
        Sets the items of the QComboBox along with their associated userData.
        
        Args:
            items_with_data (list): A list of tuples, where each tuple contains (item, userData).
            Example: [("Item 1", 1), ("Item 2", 2), ...]
        """
        self.combobox.clear()  
        self.combobox.addItem(self.placeholder, 0)
        for item, user_data in items_with_data:
            self.combobox.addItem(item, user_data)  

    def get_selected_user_data(self):
        """
        Returns the userData associated with the currently selected item in the QComboBox.

        Returns:
            Any: The userData associated with the selected item.
        """
        index = self.combobox.currentIndex()
        if index != -1:
            return self.combobox.currentData() # Returns userData associated with the selected item
        return None  

    def get_selected_text(self):
        """
        Returns the current selected item text in the QComboBox.

        Returns:
            str: The selected item text.
        """
        return self.combobox.currentText().strip()
    
    def get_selected_index(self):
        """
        Returns the current selected item index in the QComboBox.

        Returns:
            int: The selected item index.
        """
        return self.combobox.currentIndex()

    def is_valid(self):
        """
        Validates the selection based on the 'required' flag and the custom validation function.

        Returns:
            bool: True if the selection is valid, False otherwise.
        """
        index = self.combobox.currentIndex()

        # Check if the selected item is the placeholder
        if index == 0:
            self.show_error(self.error_message)
            return False
        else:
            self.hide_error()

        # Apply custom validation function if provided
        selected_item = self.get_selected_text()
        if self.validation_func and not self.validation_func(selected_item):
            self.show_error("Invalid selection.")
            return False

        self.hide_error()
        return True

    def on_selection_changed(self, index):
        """
        Slot triggered when the selection changes in the QComboBox.
        
        Args:
            index (Any): The index of the selected item.
        """
        if self.combobox.currentIndex() == 0:
            return
        
        # Call the custom selection change function if provided
        if self.on_selection_changed_func:
            self.on_selection_changed_func(index)
    
    def show_error(self, message):
        """
        Displays the error message under the QComboBox.

        Args:
            message (str): The error message to display.
        """
        self.error_label.setText(message)
        self.error_label.show()
        self.combobox.setStyleSheet("border: 1px solid red;")

    def hide_error(self):
        """
        Hides the error message and resets the QComboBox style.
        """
        self.error_label.hide()
        self.combobox.setStyleSheet("")

    def eventFilter(self, watched, event):
        """
        Event filter to capture focus events for the QComboBox.

        Args:
            watched (QObject): The object being watched (in this case, the QComboBox).
            event (QEvent): The event that occurred.
        
        Returns:
            bool: True if the event was handled, False otherwise.
        """
        if watched == self.combobox:
            if event.type() == QEvent.FocusOut:
                self.on_focus_lost()

        return super().eventFilter(watched, event)

    def on_focus_lost(self):
        """
        Method called when the QComboBox loses focus.
        """
        if not self.is_valid():
            self.show_error("Please make a valid selection.")
        else:
            self.hide_error()

    def on_current_index_changed(self):
        """
        Validates the input as the user selects.
        """
        if not self.is_valid():
            self.show_error(self.error_message)
        else:
            self.hide_error()
        
if __name__ == "__main__":
    from imports import QApplication, QMainWindow, QPushButton
    from qt_material import apply_stylesheet
    from pyside6_custom_widgets.button import Button
    app = QApplication([])

    window = QMainWindow()
    layout = QVBoxLayout()
    # Afficher le userData de l'élément sélectionné
    def print_selected_data(key):
        print("Selected userData:", combobox.get_selected_user_data())
        if combobox.is_valid():
            print(combobox.get_selected_index())
            print(combobox.get_selected_text())
        
    # Exemple d'items provenant d'une base de données (affichage, userData)
    items_with_data = [("Apple", 1), ("Banana", 2), ("Orange", 3)]

    # Création du ComboBox personnalisé
    combobox = ComboBox(items_with_data=items_with_data, required=True, on_selection_changed_func=print_selected_data)
    
    # Ajouter le ComboBox à l'interface
    layout.addWidget(combobox)

    # Bouton pour récupérer la sélection
    button = Button(text="Print Selected Data",command=print_selected_data)
    layout.addWidget(button)

    central_widget = QWidget()
    central_widget.setLayout(layout)
    window.setCentralWidget(central_widget)
    apply_stylesheet(app,theme="light_cyan.xml")
    window.show()
    app.exec()