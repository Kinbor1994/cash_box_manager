import re
from imports import QWidget, QVBoxLayout, QLineEdit, QLabel, QEvent
from utils.qss_file_loader import load_stylesheet
        
class LineEdit(QWidget):
    """
    A custom widget for QLineEdit with built-in validation, error display, and customizable styles.

    Args:
        placeholder_text (str, optional): Placeholder text for the QLineEdit. Defaults to an empty string.
        required (bool, optional): Whether the input is required. Defaults to False.
        validation_func (callable, optional): A custom validation function. Defaults to None.
        input_type (str, optional): Type of input ('text', 'password', 'email', 'numeric'). Defaults to 'text'.
        error_message (str, optional): Custom error message to display when validation fails. Defaults to "This field is required".
        custom_style (str, optional): Custom QSS style to apply to the widget. If not provided, defaults to "line_edit.qss".
        on_text_changed_func(callable, optional): function that is triggered when the text in the QLineEdit changes.
        parent (QWidget, optional): The parent widget. Defaults to None.
    """

    def __init__(
        self,
        placeholder_text="",
        required=False,
        validation_func=None,
        input_type="text",
        error_message="This field is required",
        custom_style=None,
        on_text_changer_func = None,
        parent=None,
    ):
        super().__init__(parent)
        self.required = required
        self.validation_func = validation_func
        self.input_type = input_type
        self.error_message = error_message
        self.on_text_changer_func = on_text_changer_func
        self.error_label = QLabel()

        self.setup_widget(placeholder_text)

        # Set custom style if provided, otherwise load default style
        if custom_style:
            self.setStyleSheet(custom_style)
        else:
            self.setStyleSheet(load_stylesheet("styles/line_edit.qss"))

    def setup_widget(self, placeholder_text):
        """
        Sets up the QLineEdit widget with optional placeholder and input type.
        """
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Create QLineEdit
        self.line_edit = QLineEdit()
        self.line_edit.setFixedHeight(40)
        self.line_edit.setPlaceholderText(placeholder_text)

        # Connect the textChanged signal to the custom method
        if self.on_text_changer_func:
            self.line_edit.textChanged.connect(self.on_text_changer_func)
        self.line_edit.textChanged.connect(self.on_text_changed)
        
        # Install event filter to capture focus events
        self.line_edit.installEventFilter(self)
        
        # Set input type (text, password, etc.)
        if self.input_type == "password":
            self.line_edit.setEchoMode(QLineEdit.Password)

        # Add line edit and error label to the layout
        layout.addWidget(self.line_edit)
        layout.addWidget(self.error_label)
        self.error_label.setStyleSheet("color: red;")  # Default error message style
        self.error_label.hide()

        self.setLayout(layout)

    def get_widget(self):
        """
        Returns the main widget (self).

        Returns:
            QWidget: The main widget.
        """
        return self

    def set_placeholder_text(self, text):
        """
        Sets the placeholder text of the QLineEdit.

        Args:
            text (str): The new placeholder text.
        """
        self.line_edit.setPlaceholderText(text)

    def get_text(self):
        """
        Returns the current text in the QLineEdit.

        Returns:
            str: The current text.
        """
        return self.line_edit.text().strip()
    
    def set_text(self, text):
        """
        Sets the given text in the QLineEdit.

        Args:
            text (str): The text to be set in the QLineEdit.
        """
        self.line_edit.setText(text)

    def is_valid(self):
        """
        Validates the input based on the 'required' flag, custom validation function, and input type.
        Returns:
            bool: True if the input is valid, False otherwise.
        """
        text = self.get_text()

        # Check required condition
        if self.required and not text:
            self.show_error(self.error_message)
            return False

        # Apply custom validation function if provided
        if self.validation_func and not self.validation_func(text):
            self.show_error("Invalid input.")
            return False

        # Specific input type validation
        if self.input_type == "email" and not self.validate_email(text):
            self.show_error("Invalid email address.")
            return False
        elif self.input_type == "numeric" and not self.validate_numeric(text):
            self.show_error("Only numeric values are allowed.")
            return False

        self.hide_error()
        return True

    def validate_email(self, text):
        """
        Validates if the input is a valid email address.
        Args:
            text (str): The text input to validate.
        Returns:
            bool: True if the input is a valid email, False otherwise.
        """
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(email_regex, text) is not None

    def validate_numeric(self, text):
        """
        Validates if the input contains a valid numeric value (integers or floating point numbers).

        Args:
            text (str): The text input to validate.
        
        Returns:
            bool: True if the input contains a valid numeric value, False otherwise.
        """
        # Regular expression for validating integers and floating point numbers (positive and negative)
        numeric_regex = r'^-?\d+(\.\d+)?$'
        return re.match(numeric_regex, text) is not None

    def show_error(self, message):
        """
        Displays the error message under the QLineEdit.

        Args:
            message (str): The error message to display.
        """
        self.error_label.setText(message)
        self.error_label.show()
        self.line_edit.setStyleSheet("border: 1px solid red;")

    def hide_error(self):
        """
        Hides the error message and resets the QLineEdit style.
        """
        self.error_label.hide()
        self.line_edit.setStyleSheet("")

    def eventFilter(self, watched, event):
        """
        Event filter to capture focus events for the QLineEdit.

        Args:
            watched (QObject): The object being watched (in this case, the QLineEdit).
            event (QEvent): The event that occurred.
        
        Returns:
            bool: True if the event was handled, False otherwise.
        """
        # Check if the event is related to the QLineEdit
        if watched == self.line_edit:
            # Handle focus out event
            if event.type() == QEvent.FocusOut:
                self.on_focus_lost()

        return super().eventFilter(watched, event)

    def on_focus_lost(self):
        """
        Method called when the QLineEdit loses focus.
        """
        # Perform validation or styling updates when focus is lost
        if not self.is_valid():
            self.show_error("Input is invalid.")
        else:
            self.hide_error()
        
    def on_text_changed(self):
        """
        Validates the input as the user types.
        """
        if not self.is_valid():
            self.show_error("Input is invalid.")
        else:
            self.hide_error()
        
if __name__ == '__main__':
    from imports import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel

    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()

            self.setWindowTitle("Custom LineEdit Example")
            self.setGeometry(200, 200, 400, 300)

            # Main layout
            main_widget = QWidget()
            layout = QVBoxLayout(main_widget)

            # Email LineEdit with validation
            self.email_line_edit = LineEdit(placeholder_text="Enter your email", input_type="email", required=True, on_text_changer_func=self.hello)
            layout.addWidget(self.email_line_edit)
            # Email LineEdit with validation
            self.password_line_edit = LineEdit(placeholder_text="Enter your email", input_type="password", required=True)
            layout.addWidget(self.password_line_edit)
            

            # Numeric LineEdit with validation
            self.numeric_line_edit = LineEdit(placeholder_text="Enter a number", input_type="numeric", required=True)
            layout.addWidget(self.numeric_line_edit)

            # Simple text LineEdit without special validation
            self.text_line_edit = LineEdit(placeholder_text="Enter some text", required=False)
            layout.addWidget(self.text_line_edit)

            # Button to validate inputs
            validate_button = QPushButton("Validate")
            validate_button.clicked.connect(self.validate_inputs)
            layout.addWidget(validate_button)

            # Label to display validation results
            self.result_label = QLabel("")
            layout.addWidget(self.result_label)

            self.setCentralWidget(main_widget)
            
        def hello(self):
            print("Hello")
                
        def validate_inputs(self):
            """
            Validates the inputs of the LineEdit fields and displays the result in a QLabel.
            """
            email_valid = self.email_line_edit.is_valid()
            numeric_valid = self.numeric_line_edit.is_valid()
            text_valid = self.text_line_edit.is_valid()

            if email_valid and numeric_valid and text_valid:
                self.result_label.setText("All inputs are valid!")
                self.result_label.setStyleSheet("color: green;")
            else:
                self.result_label.setText("One or more fields are invalid.")
                self.result_label.setStyleSheet("color: red;")

    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
