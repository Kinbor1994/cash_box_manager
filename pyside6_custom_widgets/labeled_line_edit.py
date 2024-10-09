from pyside6_custom_widgets.button import Button
from imports import QWidget, QVBoxLayout
from pyside6_custom_widgets.label import Label
from pyside6_custom_widgets.line_edit import LineEdit


class LabeledLineEdit(QWidget):
    """
    A custom widget combining a Label and a LineEdit, aligned vertically.

    Args:
        label_text (str): The text for the Label.
        placeholder_text (str, optional): Placeholder text for the LineEdit. Defaults to an empty string.
        required (bool, optional): Whether the LineEdit input is required. Defaults to False.
        validation_func (callable, optional): A custom validation function for the LineEdit. Defaults to None.
        input_type (str, optional): Type of input for the LineEdit ('text', 'password', 'email', 'numeric'). Defaults to 'text'.
        error_message (str, optional): Custom error message to display when validation fails. Defaults to "This field is required".
        on_change_callback(callable, optional): function that is triggered when the text in the QLineEdit changes.
        custom_style (str, optional): Custom QSS style for the LineEdit. Defaults to None.
        parent (QWidget, optional): The parent widget. Defaults to None.
    """

    def __init__(
        self,
        label_text,
        placeholder_text="",
        required=False,
        validation_func=None,
        input_type="text",
        error_message="This field is required",
        on_change_callback=None,
        custom_style=None,
        parent=None,
    ):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(2)
        if on_change_callback:
            self.on_change_callback = on_change_callback
        
        self.input_type = input_type
        # Create the custom Label and LineEdit widgets
        self.label = Label(label_text)
        self.line_edit = LineEdit(
            placeholder_text=placeholder_text,
            required=required,
            validation_func=validation_func,
            input_type=self.input_type,
            error_message=error_message,
            on_text_changer_func=on_change_callback,
            custom_style=custom_style,
        )

        # Add Label and LineEdit to the layout
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.line_edit)

        self.setLayout(self.layout)
        self.layout.addStretch(1)
        
    def get_text(self):
        """
        Returns the text from the LineEdit.

        Returns:
            str: The current text in the LineEdit.
        """
        return self.line_edit.get_text()

    def get_value(self):
        """
        Returns the text from the LineEdit.

        Returns:
            str: The current text in the LineEdit.
        """
        return self.line_edit.get_text()
    
    def set_value(self, text):
        """
        Sets the text of the LineEdit.

        Args:
            text: The text to set in the LineEdit.
        """
        self.line_edit.line_edit.setText(str(text))
        
    def set_text(self, text):
        """
        Sets the text in the LineEdit.

        Args:
            text (str): The text to set in the LineEdit.
        """
        self.line_edit.set_text(text)

    def set_label_text(self, text):
        """
        Sets the text in the Label.

        Args:
            text (str): The text to set in the Label.
        """
        self.label.set_text(text)

    def is_valid(self):
        """
        Validates the input in the LineEdit.

        Returns:
            bool: True if the input is valid, False otherwise.
        """
        return self.line_edit.is_valid()

    def on_change(self, callback):
        if callback:
            self.line_edit.line_edit.textChanged.connect(callback)

    def clear_content(self):
        self.line_edit.clear_content()
        
if __name__ == "__main__":
    from imports import QApplication, QMainWindow, QVBoxLayout, QWidget
    import sys

    app = QApplication([])

    window = QMainWindow()
    layout = QVBoxLayout()

    # Example of a labeled line edit
    labeled_line_edit = LabeledLineEdit("Username:", placeholder_text="Enter your username", required=True)
    labeled_line_edit2= LabeledLineEdit("First Name:", placeholder_text="Enter your first name", required=True, input_type="numeric")
    labeled_line_edit.set_value("Bonjour")
    btn = Button(text="Submit")
    btn2 = Button(text="Cancel",theme_color="danger")
    layout.addWidget(labeled_line_edit)
    layout.addWidget(labeled_line_edit2)
    layout.addWidget(btn)
    layout.addWidget(btn2)

    central_widget = QWidget()
    central_widget.setLayout(layout)
    window.setCentralWidget(central_widget)

    window.show()
    sys.exit(app.exec())