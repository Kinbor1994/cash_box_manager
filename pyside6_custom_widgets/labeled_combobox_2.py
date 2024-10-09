from imports import QWidget, QVBoxLayout
from pyside6_custom_widgets.label import Label
from pyside6_custom_widgets.combobox_2 import ComboBox


class LabeledComboBox(QWidget):
    """
    A custom widget combining a Label and a ComboBox, aligned vertically.

    Args:
        label_text (str): The text for the Label.
        items (list): A list of items in different formats (tuples, dicts, objects, strings, etc...). Default to [].
        placeholder (str, optional): Placeholder text for the ComboBox. Defaults to "Select an option".
        required (bool, optional): Whether the ComboBox selection is required. Defaults to False.
        validation_func (callable, optional): A custom validation function for the ComboBox. Defaults to None.
        error_message (str, optional): Custom error message to display when validation fails. Defaults to "Please select an option".
        on_change_callback(callable, optional): function that is triggered when the selection text in the QComboBoxEdit changes.
        custom_style (str, optional): Custom QSS style for the ComboBox. Defaults to None.
        parent (QWidget, optional): The parent widget. Defaults to None.
    """

    def __init__(
        self,
        label_text,
        items=[],
        placeholder="Select an option",
        required=False,
        validation_func=None,
        error_message="Please select an option",
        on_change_callback=None,
        custom_style=None,
        parent=None,
    ):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(2)
        
        self.on_change_callback = on_change_callback
        # Create the custom Label and ComboBox widgets
        self.label = Label(label_text)
        self.combobox = ComboBox(
            items=items,
            placeholder=placeholder,
            required=required,
            validation_func=validation_func,
            error_message=error_message,
            on_selection_changed_func=self.on_change_callback,
            custom_style=custom_style,
        )

        # Add Label and ComboBox to the layout
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.combobox)

        self.setLayout(self.layout)
        self.layout.addStretch(1)
        
    def get_selected_user_data(self):
        """
        Returns the userData associated with the currently selected item in the ComboBox.

        Returns:
            Any: The userData associated with the selected item.
        """
        return self.combobox.get_selected_user_data()

    def get_selected_text(self):
        """
        Returns the current selected item text in the ComboBox.

        Returns:
            str: The selected item text.
        """
        return self.combobox.get_selected_text()

    def get_value(self):
        """
        Returns the current selected item associated userData in the ComboBox.

        Returns:
            any: The selected item associated userDate.
        """
        return self.combobox.get_selected_user_data()
    
    def set_value(self, text):
        """
        Sets the current text of the ComboBox.

        Args:
            text (str): A text to set as the combobox current text.
        """
        self.combobox.combobox.setCurrentText(text)
        
    def set_items(self, items):
        """
        Sets the items of the ComboBox.

        Args:
            items (list): A list of items in different formats (tuples, dicts, objects, strings, etc.).
        """
        self.combobox.set_items(items)

    def is_valid(self):
        """
        Validates the selection in the ComboBox.

        Returns:
            bool: True if the selection is valid, False otherwise.
        """
        return self.combobox.is_valid()

    def set_label_text(self, text):
        """
        Sets the text of the Label.

        Args:
            text (str): The new text for the Label.
        """
        self.label.set_text(text)

    def on_change(self, callback):
        if callback:
            self.combobox.combobox.currentIndexChanged.connect(callback)
            
    def clear_content(self):
        self.combobox.clear_content()
        
if __name__ == "__main__":
    from imports import QApplication, QMainWindow, QVBoxLayout, QWidget
    import sys

    app = QApplication([])

    window = QMainWindow()
    layout = QVBoxLayout()

    # Example of a labeled combobox
    items_with_data = [("Apple", 1), ("Banana", 2), ("Orange", 3)]
    labeled_combobox = LabeledComboBox("Select a fruit:", items=items_with_data, required=True)
    labeled_combobox.set_value("Bonjour")
    layout.addWidget(labeled_combobox)

    central_widget = QWidget()
    central_widget.setLayout(layout)
    window.setCentralWidget(central_widget)

    window.show()
    sys.exit(app.exec())
