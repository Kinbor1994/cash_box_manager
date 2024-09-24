from datetime import datetime
from imports import QWidget, QVBoxLayout, QDate
from pyside6_custom_widgets.label import Label
from pyside6_custom_widgets.date_edit import DateEdit


class LabeledDateEdit(QWidget):
    """
    A custom widget combining a Label and a DateEdit, aligned vertically.

    Args:
        label_text (str): The text for the Label.
        required (bool, optional): Whether the date selection is required. Defaults to False.
        min_date (QDate, optional): The minimum date that can be selected. Defaults to None.
        max_date (QDate, optional): The maximum date that can be selected. Defaults to None.
        format (str, optional): The display format for the DateEdit. Defaults to "dd/MM/yyyy".
        validation_func (callable, optional): A custom validation function for the DateEdit. Defaults to None.
        error_message (str, optional): Custom error message to display when validation fails. Defaults to "Invalid date".
        on_change_callback(callable, optional): function that is triggered when the date in the QDateEdit changes.
        custom_style (str, optional): Custom QSS style for the DateEdit. Defaults to None.
        parent (QWidget, optional): The parent widget. Defaults to None.
    """

    def __init__(
        self,
        label_text,
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
        super().__init__()

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(2)
        
        self.on_change_callback = on_change_callback
        # Create the custom Label and DateEdit widgets
        self.label = Label(label_text)
        self.date_edit = DateEdit(
            required=required,
            min_date=min_date,
            max_date=max_date,
            format=format,
            validation_func=validation_func,
            error_message=error_message,
            on_change_callback=self.on_change_callback,
            custom_style=custom_style,
        )

        # Add Label and DateEdit to the layout
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.date_edit)

        self.setLayout(self.layout)
        self.layout.addStretch(1)
        
    def get_date(self):
        """
        Returns the currently selected date from the DateEdit.

        Returns:
            QDate: The currently selected date.
        """
        return self.date_edit.get_date()

    def get_value(self):
        """
        Returns the currently selected date from the DateEdit.

        Returns:
            QDate: The currently selected date.
        """
        return self.date_edit.get_date()
    
    def set_value(self, date):
        """
        Sets the date of the DateEdit.

        Args:
            date (QDate): The date to set.
        """
        self.date_edit.date_edit.setDate(date)
        
    def set_date(self, date):
        """
        Sets the date in the DateEdit.

        Args:
            date (QDate): The date to set in the DateEdit.
        """
        self.date_edit.set_date(date)

    def is_valid(self):
        """
        Validates the selected date in the DateEdit.

        Returns:
            bool: True if the selected date is valid, False otherwise.
        """
        return self.date_edit.is_valid()

    def set_label_text(self, text):
        """
        Sets the text in the Label.

        Args:
            text (str): The text to set in the Label.
        """
        self.label.set_text(text)

    def on_change(self, callback):
        if callback:
            self.date_edit.date_edit.dateChanged.connect(callback)

    def clear_content(self):
        self.date_edit.clear_content()
        
if __name__ == "__main__":
    from imports import QApplication, QMainWindow, QVBoxLayout, QWidget
    import sys

    app = QApplication([])

    window = QMainWindow()
    layout = QVBoxLayout()

    # Example of a labeled date edit
    min_date = QDate(1995, 1, 1)
    max_date = QDate(2025, 12, 31)

    labeled_date_edit = LabeledDateEdit(
        "Select a date:", required=True, min_date=min_date, max_date=max_date
    )
    labeled_date_edit.set_value(QDate(2012,5,25))
    layout.addWidget(labeled_date_edit)

    central_widget = QWidget()
    central_widget.setLayout(layout)
    window.setCentralWidget(central_widget)

    window.show()
    sys.exit(app.exec())
