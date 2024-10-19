from sqlalchemy import Date, DateTime
from babel.numbers import format_decimal

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QHBoxLayout,
    QMessageBox,
)

from pyside6_custom_widgets.button import Button
from pyside6_custom_widgets.date_edit import DateEdit
from pyside6_custom_widgets.label import Label
from pyside6_custom_widgets.combobox_3 import ComboBox
from pyside6_custom_widgets.line_edit import LineEdit
from pyside6_custom_widgets.widget_items_button import ActionButtonsWidget, ActionButtonsWidget2
from utils.qss_file_loader import load_stylesheet


class CustomTableWidget(QWidget):
    """
    A custom widget for QTableWidget that handles model instances with search, pagination, edit/delete functionality, and customizable styles.

    Args:
        model (SQLAlchemy Model): The SQLAlchemy model to display.
        columns (list, optional): A list of columns to display. If not provided, all columns will be displayed.
        edit_column (bool, optional): Whether to add an edit/delete column. Defaults to True.
        formatter (dict, optional): A dictionary where the key is the column index and the value is a formatting function.
        edit_callback (callable, optional): The function to call when the edit button is clicked.
        delete_callback (callable, optional): The function to call when the delete button is clicked.
        custom_style (str, optional): Custom QSS style to apply to the widget. Defaults to None.
        enable_pagination (bool, optional): Whether to enable pagination. Defaults to True.
        items_per_page (int, optional): The number of items to display per page. Defaults to 10.
        parent (QWidget, optional): The parent widget. Defaults to None.
    """

    def __init__(
        self,
        model,
        controller=None,
        edit_column=True,
        formatter=None,
        edit_callback=None,
        delete_callback=None,
        create_command=None,
        custom_style=None,
        enable_pagination=True,
        items_per_page=10,
    ):
        super().__init__()

        self.model = model
        self.controller = controller
        self.columns = self._get_columns()
        self.edit_column = edit_column
        self.formatter = formatter or {}
        self.edit_callback = edit_callback
        self.delete_callback = delete_callback
        self.create_button_command = create_command
        self.items_per_page = items_per_page
        self.current_page = 0
        self.current_combo_filter_name = None
        self.instances = self._get_instances()
        self.filtered_instances = self._get_instances()

        self.enable_pagination = enable_pagination
        self.amount_total_label = Label(text="", icon_name="fa.money", theme_name="success")
        self.setup_table_widget()

        # Populate the table with instances
        self.update_pagination()

        # Apply custom style if provided
        if custom_style:
            self.setStyleSheet(custom_style)
        else:
            self.setStyleSheet(load_stylesheet("styles/table_widget.qss"))

    def setup_table_widget(self):
        """
        Sets up the table widget, search bar, and pagination controls.
        """
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # widgets for filtering table data
        self.filter_layout = QHBoxLayout()
        self.create_button = Button(
            text="",
            icon_name="fa.plus",
            command=self.create_button_command,
            theme_color="success",
        )
        self.cancel_filter_button = Button(
            text="",
            icon_name="fa.times-circle",
            command=self.refresh_data,
            theme_color="secondary",
        )
        self.search_bar = LineEdit(
            placeholder_text="Search...", on_text_changer_func=self.filter_data
        )
        self.search_bar.setFixedWidth(250)
        self.filter_layout.addWidget(self.create_button)
        self.filter_layout.addWidget(self.cancel_filter_button)
        self.filter_layout.addWidget(self.search_bar)
        self.add_dynamic_filters()
        self.filter_layout.addStretch()
        # Table setup
        self.table = QTableWidget()
        self._set_headers()

        if "Actions" in self.headers:
            action_col_index = self.headers.index("Actions")
            self.table.setColumnWidth(
                action_col_index, 110
            )  # Fixed width for 'Actions'

            # Set all columns to stretch, except for the 'Actions' column
            header = self.table.horizontalHeader()
            for i in range(len(self.headers)):
                if i != action_col_index:
                    header.setSectionResizeMode(
                        i, QHeaderView.Stretch
                    )  # Other columns stretch to fill the space

            # Set the 'Actions' column to have a fixed size
            header.setSectionResizeMode(action_col_index, QHeaderView.Fixed)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)  # Select whole rows
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)

        # Add search bar and table to the layout
        self.layout.addLayout(self.filter_layout)
        self.layout.addWidget(self.table)

        self.pagination_layout = QHBoxLayout()
        if self.enable_pagination:
            self.prev_button = Button(
                text="", command=self.show_prev_page, icon_name="fa5s.arrow-left"
            )
            self.prev_button.setFixedSize(30, 30)
            self.next_button = Button(
                text="", command=self.show_next_page, icon_name="fa5s.arrow-right"
            )
            self.next_button.setFixedSize(30, 30)
            self.pagination_layout.addWidget(self.prev_button)
            self.pagination_layout.addWidget(self.next_button)

        # Add label for pagination info
        self.pagination_info_label = Label(text="", theme_name="success")
        self.pagination_layout.addWidget(self.pagination_info_label)
        self.pagination_layout.addWidget(self.amount_total_label)

        self.layout.addLayout(self.pagination_layout)

    def _set_headers(self):
        """
        Sets the column headers for the QTableWidget.

        Args:
            headers (list): A list of column headers.
        """
        self.headers = self._get_headers()
        if self.edit_column and "Actions" not in self.headers:
            self.headers.append("Actions")

        self.table.setColumnCount(len(self.headers))
        self.table.setHorizontalHeaderLabels(self.headers)

    def add_dynamic_filters(self):
        """
        Adds dynamic filter widgets (LabeledComboBox and LabeledDateEdit) for ForeignKey and Date columns.
        """
        columns = sorted(
            [col for col in self.model.__table__.columns if col.name != "id"],
            key=lambda col: col.info.get("tab_col_index", 0),
        )
        for col in columns:
            editable = col.info.get("editable", "true") != "false"
            if not editable:
                continue

            if col.foreign_keys:  # ForeignKey detection
                self.current_combo_filter_name = col.name
                combo_filter = ComboBox(
                    items=self.get_cbx_items(col.name),
                    placeholder="Choissez un élement pour filtrer....",
                    on_selection_changed_func=self.filter_by_category,
                )
                combo_filter.setObjectName(col.name)
                combo_filter.setFixedWidth(300)
                self.filter_layout.addWidget(combo_filter)
            elif isinstance(col.type, (Date, DateTime)):
                self.current_start_filter_date = f"start_{col.name}"
                self.current_end_filter_date = f"end_{col.name}"
                start_date_filter = DateEdit(
                    required=False, on_change_callback=self.filter_by_period
                )
                start_date_filter.setObjectName(f"start_{col.name}")
                start_date_filter.setFixedWidth(150)
                end_date_filter = DateEdit(
                    required=False, on_change_callback=self.filter_by_period
                )
                end_date_filter.setObjectName(f"end_{col.name}")
                end_date_filter.setFixedWidth(150)
                self.filter_layout.addWidget(start_date_filter)
                self.filter_layout.addWidget(end_date_filter)

    def format_value(self, value, col):
        """
        Automatically formats value based on type or applies custom formatter.
        """
        if col in self.formatter:
            return self.formatter[col](value)  # Apply custom formatter

        if isinstance(value, (int, float)):  # Format numbers with thousand separators
            return format_decimal(value, locale="fr_FR")
        elif isinstance(value, Date):  # Format dates
            return value.strftime("%d/%m/%Y")
        elif isinstance(value, DateTime):
            return value.strftime("%d/%m/%Y %H:%M")
        else:
            return str(value)

    def populate_table(self, instances):
        self.table.setRowCount(0)
        id_col_index = self.headers.index("id")
        for row_idx, instance in enumerate(instances):
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            for col_idx, col in enumerate(self.columns):
                value = self.get_column_value(instance, col)
                formatted_value = self.format_value(value, col_idx)
                self.table.setItem(
                    row_position, col_idx, QTableWidgetItem(formatted_value)
                )
                if row_position == id_col_index:
                    self.table.setColumnHidden(row_position, True)

            if self.edit_column:
                action_widget = ActionButtonsWidget(
                    modify_callback=lambda _, r=instance.id: (
                        self.edit_callback(r) if self.edit_callback else None
                    ),
                    delete_callback=lambda _, r=instance.id: (
                        self.delete_callback(r)
                        if self.delete_callback
                        else self.delete_instance
                    ),
                )
                self.table.setCellWidget(
                    row_position, len(self.headers) - 1, action_widget
                )
                self.table.setRowHeight(row_position, 50)

    def get_column_value(self, instance, column):
        """
        Retrieves the value for a specific column from the instance. If the column is a ForeignKey,
        it will return the specified field of the related model instead of the ID.

        Args:
            instance (object): The SQLAlchemy model instance.
            column (str): The column name.

        Returns:
            str: The value to display in the table for the column.
        """
        if column != "Actions":
            value = getattr(instance, column, "")

            # Check if the column has a ForeignKey relationship
            column_info = self.model.__table__.columns[column].info
            if "related_column" in column_info:
                # Get the related instance
                related_instance = getattr(instance, column.replace("_id", ""), None)
                if related_instance:
                    # Get the specified field from the related instance
                    related_column = column_info["related_column"]
                    value = getattr(related_instance, related_column, "")

            return value

    def _get_instances(self):
        instances = self.controller.get_all()
        return instances

    def _get_columns(self):
        """
        Récupère et trie les colonnes du modèle SQLAlchemy en fonction de `tab_col_index`.
        Les colonnes avec des valeurs négatives de `tab_col_index` apparaissent à la fin.
        """
        # Récupérer toutes les colonnes avec leur ordre `tab_col_index` spécifié dans le modèle
        columns_with_order = [
            (col.info.get("tab_col_index", index), col.name)
            for index, col in enumerate(self.model.__table__.columns)
        ]

        # Séparer les colonnes avec des index négatifs (qui iront en dernier) et positifs/nuls
        positive_columns = [
            (index, name) for index, name in columns_with_order if index >= 0
        ]
        negative_columns = [
            (index, name) for index, name in columns_with_order if index < 0
        ]

        # Trier les colonnes positives par `tab_col_index` croissant et les négatives également
        sorted_positive_columns = sorted(positive_columns)
        sorted_negative_columns = sorted(negative_columns)

        # Combiner les colonnes positives d'abord, puis les négatives
        sorted_columns = [
            col_name
            for _, col_name in sorted_positive_columns + sorted_negative_columns
        ]

        return sorted_columns

    def _get_headers(self):

        columns_with_order = [
            (
                col.info.get("tab_col_index", index),
                col.info.get("verbose_name", col.name),
            )
            for index, col in enumerate(self.model.__table__.columns)
        ]

        positive_columns = [
            (index, name) for index, name in columns_with_order if index >= 0
        ]
        negative_columns = [
            (index, name) for index, name in columns_with_order if index < 0
        ]

        sorted_positive_columns = sorted(positive_columns)
        sorted_negative_columns = sorted(negative_columns)

        sorted_columns = [
            col_name
            for _, col_name in sorted_positive_columns + sorted_negative_columns
        ]

        return sorted_columns

    def _set_data(self):
        """
        Sets the table data and refreshes the table.

        Args:
            instances (list): A list of model instances.
        """
        self.instances = self._get_instances()
        self.filtered_instances = self._get_instances()
        self.update_pagination()

    def refresh_data(self):
        """
        Refresh the data displayed in the table.
        """
        self._set_data()
        self.update_combobox_items()

    def filter_data(self):
        """
        Filters the table data based on the search text.
        """
        search_text = self.search_bar.get_text().lower()

        if search_text:
            self.filtered_instances = [
                instance
                for instance in self.instances
                if self.instance_matches_search(instance, search_text)
            ]
        else:
            self.filtered_instances = self.instances

        self.update_pagination()

    def filter_by_category(self):
        cbx = self.findChild(ComboBox, self.current_combo_filter_name)
        id = cbx.get_selected_user_data() if cbx else ""

        if id:
            self.filtered_instances = self.controller.get_filter_by_category_id(id)
        else:
            self.filtered_instances = self.instances

        self.update_pagination()

    def filter_by_period(self):
        start_date_edit = self.findChild(DateEdit, self.current_start_filter_date)
        end_date_edit = self.findChild(DateEdit, self.current_end_filter_date)
        start_date = start_date_edit.get_date()
        end_date = end_date_edit.get_date()
        self.filtered_instances = self.controller.get_filter_by_period(
            start_date, end_date
        )
        self.update_pagination()

    def instance_matches_search(self, instance, search_text):
        """
        Checks if an instance matches the search text.

        Args:
            instance (object): The instance of the SQLAlchemy model.
            search_text (str): The search input text.

        Returns:
            bool: True if the instance matches the search text, False otherwise.
        """
        # Exclude the 'Actions' column from the search
        searchable_columns = [col for col in self.columns if col != "Actions"]

        return any(
            search_text in str(getattr(instance, col)).lower()
            for col in searchable_columns
        )

    def update_pagination(self):
        """
        Updates the table to display only the rows for the current page.
        """
        if self.enable_pagination:
            start_row = self.current_page * self.items_per_page
            end_row = start_row + self.items_per_page
            paginated_instances = self.filtered_instances[
                start_row:end_row
            ]  # Show only a subset of instances
        else:
            # If pagination is disabled, show all rows
            paginated_instances = self.filtered_instances

        self.populate_table(paginated_instances)

        # Update pagination info
        total_items = len(self.filtered_instances)

        if self.enable_pagination:
            current_items = len(paginated_instances)
            total_pages = (total_items // self.items_per_page) + (
                1 if total_items % self.items_per_page != 0 else 0
            )
            current_page = self.current_page + 1  # Pages are 1-based

            self.pagination_info_label.setText(
                f"Showing {start_row + 1} to {start_row + current_items} of {total_items} rows | Page {current_page} of {total_pages}"
            )
        else:
            # When pagination is disabled, show the total number of items
            self.pagination_info_label.setText(f"Showing all {total_items} rows")
        self.update_amount_total()

    def update_amount_total(self):
        """
        Updates the label to show the total amount of the filtered rows if the 'amount' column exists.
        """
        if "amount" in self.columns:
            total = sum(getattr(instance, "amount", 0) for instance in self.filtered_instances)
            self.amount_total_label.setText(f"Total Amount: {format_decimal(total, locale='fr_FR')}")
        else:
            self.amount_total_label.clear()
            
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
        if (self.current_page + 1) * self.items_per_page < len(self.filtered_instances):
            self.current_page += 1
            self.update_pagination()

    def delete_instance(self, instance_id):
        """
        Handles the deletion of a database instance.

        Args:
            instance_id (int): The ID of the instance to delete.
        """
        try:
            reply = QMessageBox.question(
                self,
                "Suppression",
                f"Êtes-vous sûr de vouloir supprimer cette ligne de la base de données ?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                response = self.controller.delete(instance_id)
                if response:
                    QMessageBox.information(
                        self, "Success", "Suppression effectuée avec succès."
                    )
                else:
                    QMessageBox.critical(
                        self,
                        "Erreur",
                        "Une erreur est survenue de la suppression de cette entrée.",
                    )
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Error deleting instance: {e}")

    def update_combobox_items(self):
        """
        Update the items of the ComboBox filters when data changes.
        """
        combo_filter = self.findChild(ComboBox, self.current_combo_filter_name)
        if combo_filter:
            new_items = self.get_cbx_items(self.current_combo_filter_name)
            combo_filter.combobox.clear()  # Clear existing items
            combo_filter.set_items(new_items)  # Add updated items

    def get_cbx_items(self, column_name):
        object_list = self.controller.get_related_model_all(column_name)
        if object_list:
            return object_list
        else:
            return []
