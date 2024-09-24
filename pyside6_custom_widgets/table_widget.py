from pyside6_custom_widgets.button import Button
from imports import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout
from pyside6_custom_widgets.label import Label
from pyside6_custom_widgets.line_edit import LineEdit
from pyside6_custom_widgets.widget_items_button import ActionButtonsWidget

class CustomTableWidget(QWidget):
    """
    A custom widget for QTableWidget with built-in search, pagination, edit/delete column, validation, and customizable styles.
    
    Args:
        headers (list): A list of column headers.
        data (list of tuples or dict): The table data. Example: [("Row1 Col1", "Row1 Col2"), ...] or [{"col1": value, "col2": value}, ...]
        formatter (dict, optional): A dictionary where the key is the column index and the value is a formatting function.
        edit_column (bool, optional): Whether to add an edit/delete column. Defaults to True.
        edit_callback (callable, optional): The function to call when the edit button is clicked.
        delete_callback (callable, optional): The function to call when the delete button is clicked.
        custom_style (str, optional): Custom QSS style to apply to the widget. If not provided, defaults to "table_widget.qss".
        enable_pagination (bool, optional): Whether to enable pagination. Defaults to True.
        items_per_page (int, optional): The number of item to display per page. Defaults to 10
        parent (QWidget, optional): The parent widget. Defaults to None.
    """

    def __init__(self, headers=[], data=[], formatter=None, edit_column=True, edit_callback=None, delete_callback=None, custom_style=None, enable_pagination=True, items_per_page=10, parent=None):
        super().__init__(parent)
        
        self.headers = headers
        self.data = data
        self.formatter = formatter
        self.edit_column = edit_column
        self.edit_callback = edit_callback
        self.delete_callback = delete_callback
        self.filtered_data = data  # Store filtered data for search functionality
        self.items_per_page = items_per_page
        self.current_page = 0
        
        self.enable_pagination = enable_pagination
        self.setup_table_widget()

        # Populate the table with data
        self.update_pagination()

        # Apply custom style if provided
        if custom_style:
            self.setStyleSheet(custom_style)
        else:
            self.setStyleSheet("")

    def setup_table_widget(self):
        """
        Sets up the table widget, search bar, and pagination controls.
        """
        # Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Search bar for filtering table data
        self.search_layout = QHBoxLayout()
        self.search_bar = LineEdit(placeholder_text="Search...", on_text_changer_func=self.filter_data)
        self.search_layout.addWidget(self.search_bar)
        # Create the QTableWidget
        self.table = QTableWidget()
        self.set_headers(self.headers)  # Set the headers including "Actions" if needed
        # Fixing the width of the 'Actions' column, and allowing other columns to stretch
        if "Actions" in self.headers:
            action_col_index = self.headers.index("Actions")
            self.table.setColumnWidth(action_col_index, 110)  # Fixed width for 'Actions'

            # Set all columns to stretch, except for the 'Actions' column
            header = self.table.horizontalHeader()
            for i in range(len(self.headers)):
                if i != action_col_index:
                    header.setSectionResizeMode(i, QHeaderView.Stretch)  # Other columns stretch to fill the space

            # Set the 'Actions' column to have a fixed size
            header.setSectionResizeMode(action_col_index, QHeaderView.Fixed)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)  # Select whole rows
        self.table.setAlternatingRowColors(True)  # Alternate row colors

        # Add search bar and table to the layout
        self.layout.addLayout(self.search_layout)
        self.layout.addWidget(self.table)

        self.pagination_layout = QHBoxLayout()
        if self.enable_pagination:
            self.prev_button = Button(text="", command=self.show_prev_page, icon_name="fa5s.arrow-left")
            self.prev_button.setFixedSize(30,30)
            self.next_button = Button(text="", command=self.show_next_page, icon_name="fa5s.arrow-right")
            self.next_button.setFixedSize(30,30)
            self.pagination_layout.addWidget(self.prev_button)
            self.pagination_layout.addWidget(self.next_button)
            
        # Add label for pagination info
        self.pagination_info_label = Label(text="",theme_name="success")
        self.pagination_layout.addWidget(self.pagination_info_label)

        self.layout.addLayout(self.pagination_layout)

    def populate_table(self, data):
        """
        Populates the QTableWidget with the provided data, applying optional formatting and adding edit/delete buttons.

        Args:
            data (list): A list of tuples or dictionaries with the table data.
        """
        self.table.setRowCount(0)  # Clear existing rows

        for row_idx, row_data in enumerate(data):
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            # If data is in tuple format
            if isinstance(row_data, (list, tuple)):
                for col_idx, item in enumerate(row_data):
                    formatted_value = self.formatter[col_idx](item) if self.formatter and col_idx in self.formatter else str(item)
                    self.table.setItem(row_position, col_idx, QTableWidgetItem(formatted_value))

            # If data is in dictionary format
            elif isinstance(row_data, dict):
                for col_idx, header in enumerate(self.headers):
                    value = row_data.get(header, "")
                    formatted_value = self.formatter[col_idx](value) if self.formatter and col_idx in self.formatter else str(value)
                    self.table.setItem(row_position, col_idx, QTableWidgetItem(formatted_value))

            # Add edit and delete buttons if edit_column is True
            if self.edit_column:
                action_widget = ActionButtonsWidget(
                    modify_callback=lambda _, r=row_idx: self.edit_callback(r) if self.edit_callback else None,
                    delete_callback=lambda _, r=row_idx: self.delete_callback(r) if self.delete_callback else None
                )
                self.table.setCellWidget(row_position, len(self.headers) - 1, action_widget)
                self.table.setRowHeight(row_position, 50)
        
    def set_data(self, data):
        """
        Sets the table data and refreshes the table.

        Args:
            data (list): A list of tuples or dictionaries with the table data.
        """
        self.data = data
        self.filtered_data = data
        self.update_pagination()

    def filter_data(self):
        """
        Filters the table data based on the search text.
        """
        search_text = self.search_bar.get_text().lower()

        if search_text:
            self.filtered_data = [row for row in self.data if self.row_matches_search(row, search_text)]
        else:
            self.filtered_data = self.data

        self.update_pagination()

    def row_matches_search(self, row_data, search_text):
        """
        Checks if a row matches the search text.

        Args:
            row_data (tuple or dict): The data for a single row.
            search_text (str): The search input text.

        Returns:
            bool: True if the row matches the search text, False otherwise.
        """
        # For tuple or list row data
        if isinstance(row_data, (list, tuple)):
            return any(search_text in str(cell).lower() for cell in row_data)

        # For dictionary row data
        elif isinstance(row_data, dict):
            return any(search_text in str(value).lower() for value in row_data.values())

    def update_pagination(self):
        """
        Updates the table to display only the rows for the current page.
        """
        if self.enable_pagination:
            start_row = self.current_page * self.items_per_page
            end_row = start_row + self.items_per_page
            paginated_data = self.filtered_data[start_row:end_row]  # Show only a subset of data
        else:
            # If pagination is disabled, show all rows
            paginated_data = self.filtered_data

        self.populate_table(paginated_data)

        # Update pagination info (always show total rows, even if pagination is disabled)
        total_items = len(self.filtered_data)
        
        if self.enable_pagination:
            current_items = len(paginated_data)
            total_pages = (total_items // self.items_per_page) + (1 if total_items % self.items_per_page != 0 else 0)
            current_page = self.current_page + 1  # Pages are 1-based

            self.pagination_info_label.setText(f"Showing {start_row + 1} to {start_row + current_items} of {total_items} rows | Page {current_page} of {total_pages}")
        else:
            # When pagination is disabled, show the total number of items
            self.pagination_info_label.setText(f"Showing all {total_items} rows")
            
    def show_prev_page(self):
        """
        Shows the previous page of the table.
        """
        if self.current_page > 0:
            self.current_page -= 1
            self.update_pagination()

    def show_next_page(self):
        """
        Shows the next page of the table.
        """
        if (self.current_page + 1) * self.items_per_page < len(self.filtered_data):
            self.current_page += 1
            self.update_pagination()

    def set_headers(self, headers):
        """
        Sets the column headers for the QTableWidget.

        Args:
            headers (list): A list of column headers.
        """
        self.headers = headers
        if self.edit_column and "Actions" not in self.headers:
            self.headers.append("Actions")
        
        self.table.setColumnCount(len(self.headers))
        self.table.setHorizontalHeaderLabels(self.headers)


# if __name__ == "__main__":
#     from imports import QApplication, QMainWindow, QVBoxLayout, QWidget
#     import sys
#     from qt_material import apply_stylesheet
#     from data import data

#     def format_age(age):
#         return f"{age} years old" if isinstance(age, int) else age
    
#     def format_job(job):
#         return f"{job} - IBM" if isinstance(job, str) else job

#     def edit_row(row):
#         print(f"Name: {custom_table.table.item(row, 0).text()}")
#         print(f"Age: {custom_table.table.item(row, 1).text()}")
#         print(f"Occupation: {custom_table.table.item(row, 2).text()}")

#     def delete_row(row):
#         print(f"Deleting row {row}")

#     app = QApplication([])

#     window = QMainWindow()
#     layout = QVBoxLayout()

#     # Example data for the table
#     headers = ["Name", "Age", "Occupation"]
#     but = Button(text="Bonjour",icon_name="fa5s.home")
#     # Formatter dictionary
#     formatter = {1: format_age,2:format_job}

#     # Create the CustomTableWidget with headers and data
#     custom_table = CustomTableWidget(headers=headers, data=data, formatter=formatter, edit_column=True, edit_callback=edit_row, delete_callback=delete_row, enable_pagination=True, items_per_page=25)
#     custom_table.search_layout.addWidget(but)

#     layout.addWidget(custom_table)

#     central_widget = QWidget()
#     central_widget.setLayout(layout)
#     window.setCentralWidget(central_widget)
#     apply_stylesheet(app,theme="dark_teal.xml")
#     window.resize(600, 400)
#     window.show()

#     sys.exit(app.exec())
