from imports import QWidget, QVBoxLayout, QComboBox, QLabel, QCompleter
from PySide6.QtCore import Qt, QStringListModel

from utils.qss_file_loader import load_stylesheet

class ComboBox(QWidget):
    """
    A custom widget for QComboBox with integrated search functionality using QCompleter.
    
    Args:
        items (list): A list of items in different formats (tuples, dicts, objects, strings, etc.). Default to [].
        custom_style (str, optional): Custom QSS style to apply to the widget. If not provided, defaults to "combobox.qss".
        on_selection_changed_func (callable, optional): Function triggered when the selection changes in the QComboBox.
        parent (QWidget, optional): The parent widget. Defaults to None.
    """

    def __init__(self, items=[], placeholder="Select an option", custom_style=None, on_selection_changed_func=None, parent=None):
        super().__init__(parent)
        self.placeholder = placeholder 
        self.on_selection_changed_func = on_selection_changed_func
        self.items = items 

        self.setup_widget()

        # Set custom style if provided, otherwise load default style
        if custom_style:
            self.setStyleSheet(custom_style)
        else:
            self.setStyleSheet(load_stylesheet("styles/combobox.qss"))

    def setup_widget(self):
        """
        Sets up the QComboBox widget with QCompleter for search functionality.
        """
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Create QComboBox in editable mode
        self.combobox = QComboBox()
        self.combobox.setEditable(True)
        self.combobox.setInsertPolicy(QComboBox.NoInsert)

        # Set up QCompleter for search functionality
        self.completer = QCompleter(self.items, self)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)  # Case insensitive search
        self.completer.setCompletionMode(QCompleter.PopupCompletion)  # Show popup with suggestions
        self.combobox.setCompleter(self.completer)

        # Set items in the combobox
        self.set_items(self.items)

        # Connect the signal for selection change to the custom method
        self.combobox.currentIndexChanged.connect(self.on_selection_changed)
        
        # Add combo box and error label to the layout
        layout.addWidget(self.combobox)

        self.setLayout(layout)

    def set_items(self, items):
        """
        Sets the items of the QComboBox along with their associated userData, handling different input formats.
        
        Args:
            items (list): A list of items in different formats (tuples, dicts, objects, strings, etc.).
                Example supported formats:
                - [("Item 1", 1), ("Item 2", 2)] (tuples)
                - [{"label": "Item 1", "value": 1}, {"label": "Item 2", "value": 2}] (dictionaries)
                - [CustomObject1, CustomObject2] (objects with custom attributes)
                - ["Item 1", "Item 2"] (simple list of strings)
        """
        self.combobox.clear()  # Clear existing items
        self.combobox.addItem(self.placeholder, 0)

        # Check the type of the first element to determine the format
        for item in items:
            if isinstance(item, tuple) and len(item) == 2:
                # If item is a tuple (label, userData)
                label, user_data = item
            elif isinstance(item, dict):
                # If item is a dictionary {"label": ..., "value": ...}
                label = item.get('label', 'Unknown')
                user_data = item.get('value', None)
            elif hasattr(item, 'title') and hasattr(item, 'id'):
                # If item is an object with 'title' and 'id' attributes (custom object)
                label = item.title
                user_data = item.id
            else:
                label = str(item)
                user_data = None

            self.combobox.addItem(label, user_data)

        # Update the completer's model with the new items (only labels)
        self.items = [self.combobox.itemText(i) for i in range(1, self.combobox.count())]
        self.completer.setModel(QStringListModel(self.items))

    def get_selected_user_data(self):
        """
        Returns the userData associated with the currently selected item in the QComboBox.

        Returns:
            Any: The userData associated with the selected item.
        """
        index = self.combobox.findText(self.combobox.currentText())
        if index != -1:
            return self.combobox.itemData(index)  # Returns userData associated with the selected item
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

    def on_selection_changed(self):
        """
        Slot triggered when the selection changes in the QComboBox.
        
        Args:
            index (Any): The index of the selected item.
        """
        if self.combobox.currentIndex() == 0:
            return 
        
        # Call the custom selection change function if provided
        if self.on_selection_changed_func:
            self.on_selection_changed_func()
    
        
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
    import sys

    app = QApplication([])

    window = QMainWindow()
    layout = QVBoxLayout()

    # Example of a ComboBox with QCompleter for search functionality
    items_with_data = [("Apple", 1), ("Banana", 2), ("Orange", 3), ("Mango", 4), ("Pineapple", 5)]
    items = [
        ("Apple", 1),  # Tuple (label, userData)
        {"label": "Banana", "value": 2},  # Dictionnaire
        "Mango",  # Simple string
    ]
    combobox_with_completer = ComboBox(items=items, on_selection_changed_func=lambda x: print(f"{x}"))

    layout.addWidget(combobox_with_completer)

    central_widget = QWidget()
    central_widget.setLayout(layout)
    window.setCentralWidget(central_widget)

    window.show()
    sys.exit(app.exec())
