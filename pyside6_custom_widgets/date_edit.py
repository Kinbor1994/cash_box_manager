from imports import QWidget, QVBoxLayout, QDateEdit, QLabel, QEvent, QDate

from utils.qss_file_loader import load_stylesheet


class DateEdit(QWidget):
    """
    A custom widget for QDateEdit with built-in validation, error display, and customizable styles.

    Args:
        required (bool, optional): Whether the date selection is required. Defaults to False.
        min_date (QDate, optional): The minimum date that can be selected. Defaults to None.
        max_date (QDate, optional): The maximum date that can be selected. Defaults to None.
        format (str, optional): The display format for the date. Defaults to "dd/MM/yyyy".
        validation_func (callable, optional): A custom validation function. Defaults to None.
        error_message (str, optional): Custom error message to display when validation fails. Defaults to "Invalid date".
        on_change_callback(callable, optional): function that is triggered when the date in the QDateEdit changes.
        custom_style (str, optional): Custom QSS style to apply to the widget. If not provided, defaults to "date_edit.qss".
        parent (QWidget, optional): The parent widget. Defaults to None.
    """

    def __init__(
        self,
        required=False,
        min_date=None,
        max_date=None,
        format="dd/MM/yyyy",
        validation_func=None,
        error_message="Invalid date",
        on_change_callback=None,
        custom_style=None,
        parent=None,
    ):
        super().__init__(parent)
        self.required = required
        self.min_date = min_date
        self.max_date = max_date
        self.validation_func = validation_func
        self.error_message = error_message
        self.error_label = QLabel()

        self.setup_widget(format)
        
        if on_change_callback:
            self.date_edit.dateChanged.connect(on_change_callback)
            
        # Set custom style if provided, otherwise load default style
        if custom_style:
            self.setStyleSheet(custom_style)
        else:
            self.setStyleSheet(load_stylesheet("styles/date_edit.qss"))

    def setup_widget(self, format):
        """
        Sets up the QDateEdit widget with optional minimum and maximum dates.
        """
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Create QDateEdit
        self.date_edit = QDateEdit()
        self.date_edit.setDisplayFormat(format)
        self.date_edit.setCalendarPopup(
            True
        )  # Show a calendar popup for date selection

        # Set minimum and maximum dates if provided
        if self.min_date:
            self.date_edit.setMinimumDate(self.min_date)
        if self.max_date:
            self.date_edit.setMaximumDate(self.max_date)

        # Connect the dateChanged signal to the validation method
        self.date_edit.dateChanged.connect(self.on_date_changed)

        # Install event filter to capture focus events
        self.date_edit.installEventFilter(self)

        # Add the date edit and error label to the layout
        layout.addWidget(self.date_edit)
        layout.addWidget(self.error_label)
        self.error_label.setStyleSheet("color: red;")  # Default error message style
        self.error_label.hide()

        self.setLayout(layout)

    def set_date(self, date):
        """
        Sets the date in the QDateEdit.

        Args:
            date (QDate): The date to set.
        """
        self.date_edit.setDate(date)

    def get_date(self):
        """
        Returns the currently selected date from the QDateEdit.

        Returns:
            QDate: The currently selected date.
        """
        return self.date_edit.date().toPython()

    def is_valid(self):
        """
        Validates the selected date based on the 'required' flag, minimum/maximum date, and the custom validation function.

        Returns:
            bool: True if the selected date is valid, False otherwise.
        """
        selected_date = self.get_date()

        # Check if the date is outside the minimum or maximum range
        if self.min_date and selected_date < self.min_date:
            self.show_error(
                f"Date must be after {self.min_date.toString('dd/MM/yyyy')}"
            )
            return False
        
        if self.max_date and selected_date > self.max_date:
            self.show_error(
                f"Date must be before {self.max_date.toString('dd/MM/yyyy')}"
            )
            return False

        # Apply custom validation function if provided
        if self.validation_func and not self.validation_func(selected_date):
            self.show_error("Invalid date selection.")
            return False

        self.hide_error()
        return True

    def on_date_changed(self, date):
        """
        Slot triggered when the date is changed in the QDateEdit.

        Args:
            date (QDate): The new date selected.
        """
        # Perform validation when the date is changed
        self.is_valid()

    def show_error(self, message):
        """
        Displays the error message under the QDateEdit.

        Args:
            message (str): The error message to display.
        """
        self.error_label.setText(message)
        self.error_label.show()
        self.date_edit.setStyleSheet("border: 1px solid red;")

    def hide_error(self):
        """
        Hides the error message and resets the QDateEdit style.
        """
        self.error_label.hide()
        self.date_edit.setStyleSheet("")

    def eventFilter(self, watched, event):
        """
        Event filter to capture focus events for the QDateEdit.

        Args:
            watched (QObject): The object being watched (in this case, the QDateEdit).
            event (QEvent): The event that occurred.

        Returns:
            bool: True if the event was handled, False otherwise.
        """
        if watched == self.date_edit:
            if event.type() == QEvent.FocusOut:
                self.on_focus_lost()

        return super().eventFilter(watched, event)

    def on_focus_lost(self):
        """
        Method called when the QDateEdit loses focus.
        """
        if not self.is_valid():
            self.show_error(self.error_message)
        else:
            self.hide_error()

    def clear_content(self):
        if self.min_date:
            self.date_edit.setDate(self.min_date)
        else:
            self.date_edit.setDate(QDate(2000, 1, 1))
            
if __name__ == "__main__":
    from imports import QApplication, QMainWindow
    from qt_material import apply_stylesheet
    
    app = QApplication([])

    window = QMainWindow()
    layout = QVBoxLayout()

    # Create a DateEdit with a minimum and maximum date
    min_date = QDate(2020, 1, 1)
    max_date = QDate(2023, 12, 31)

    date_edit = DateEdit(min_date=min_date, max_date=max_date, required=True)

    # Add the DateEdit to the layout
    layout.addWidget(date_edit)

    central_widget = QWidget()
    central_widget.setLayout(layout)
    window.setCentralWidget(central_widget)
    apply_stylesheet(app, theme="light_cyan.xml")
    window.show()
    app.exec()