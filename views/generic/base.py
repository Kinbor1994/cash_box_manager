from sqlalchemy import Date, DateTime, Enum, Float, Integer, String

from imports import QDialog, QVBoxLayout, QHBoxLayout, QFrame, QSize, QGridLayout, QSpacerItem, QSizePolicy, QMessageBox, QWidget, Signal, QCloseEvent
from pyside6_custom_widgets.button import Button
from pyside6_custom_widgets.label import Label
from pyside6_custom_widgets.labeled_combobox_2 import LabeledComboBox
from pyside6_custom_widgets.labeled_date_edit import LabeledDateEdit
from pyside6_custom_widgets.labeled_line_edit import LabeledLineEdit
from pyside6_custom_widgets.table_widget import CustomTableWidget
from utils.utils import  set_app_icon

from qt_material import apply_stylesheet

class BaseFormWidget(QDialog):
    
    def __init__(self, title="", model=None, controller=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        apply_stylesheet(self, theme="default_light.xml")
        set_app_icon(self)
        self.title = title
        self.model = model
        self.controller = controller
        self.fields = []
        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        self.main_layout = QVBoxLayout()

        self.title_label = Label(text=self.title)
        self.title_label.setProperty("role","page_title")
        self.main_layout.addWidget(self.title_label)

        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        self.main_layout.addWidget(self.separator)

        # Dynamically create fields based on the model
        self.create_fields()

        self.button_layout = QHBoxLayout()
        self.submit_btn = Button(text="Enregistrer", icon_name="fa.save", theme_color="primary")
        self.cancel_btn = Button(text="Annuler", icon_name="fa.sign-out", theme_color="danger")

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.button_layout.addItem(spacer)
        
        self.button_layout.addWidget(self.submit_btn)
        self.button_layout.addWidget(self.cancel_btn)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)

    def setup_connections(self):
        self.cancel_btn.clicked.connect(self.close)
        self.submit_btn.clicked.connect(self.submit)
        
    def create_fields(self):
        """
        Dynamically create input fields based on the model attributes, ordered by tab_col_index.
        If the number of fields exceeds 6, they are displayed in two columns.
        If the number of fields exceeds 20, they are displayed in three columns.
        """
        # Trier les colonnes du modèle en fonction de leur 'tab_col_index'
        columns = sorted(
            [col for col in self.model.__table__.columns if col.name != 'id'],
            key=lambda col: col.info.get('tab_col_index', 0)
        )

        # Déterminer le nombre de colonnes à afficher
        total_fields = len(columns)
        if total_fields > 20:
            num_columns = 3
        elif total_fields > 6:
            num_columns = 2
        else:
            num_columns = 1

        grid_layout = QGridLayout()
        row = 0
        col = 0

        for column in columns:
            field_widget = self.create_field_widget(column)

            if field_widget:
                field_widget.setObjectName(column.name)
                self.fields.append(field_widget)
                grid_layout.addWidget(field_widget, row, col)

                # Gérer le placement en colonnes
                row += 1
                if row >= total_fields // num_columns:
                    row = 0
                    col += 1

        self.main_layout.addLayout(grid_layout)

    def create_field_widget(self, column):
        """
        Create the appropriate field widget based on column attributes.
        """
        verbose_name = column.info.get("verbose_name", column.name)
        required = not column.nullable
        editable = column.info.get("editable", "true") != "false"
        input_type = column.info.get("column_type", "text")

        if required:
            verbose_name = f'{verbose_name}(*)'
    
        if not editable:
            return 

        # Handle String, Integer, Float columns without foreign keys
        if isinstance(column.type, (String, Integer, Float)) and not column.foreign_keys and input_type != "enum":
            return LabeledLineEdit(label_text=verbose_name, required=required, input_type=input_type)

        # Handle ForeignKey columns
        elif column.foreign_keys:
            return LabeledComboBox(label_text=verbose_name, items=self.get_cbx_items(column.name), required=required)

        # Handle Date or DateTime columns
        elif isinstance(column.type, (Date, DateTime)):
            return LabeledDateEdit(label_text=verbose_name, required=required)

        # Handle Enum columns (like gender)
        elif isinstance(column.type, Enum):
            return LabeledComboBox(label_text=verbose_name, items=column.type.enums, required=required)

        return None

    def create_non_editable_field(self, column, verbose_name, required):
        """
        Create a non-editable field based on the column type.
        """
        if isinstance(column.type, (String, Integer, Float)) and not column.foreign_keys:
            field_widget = LabeledLineEdit(label_text=verbose_name, required=required)
        elif column.foreign_keys:
            field_widget = LabeledComboBox(label_text=verbose_name, required=required)
        elif isinstance(column.type, (Date, DateTime)):
            field_widget = LabeledDateEdit(label_text=verbose_name, required=required)

        if field_widget:
            field_widget.setEnabled(False)
            field_widget.setVisible(False)

        return field_widget

    def get_form_data(self):
        """
        Retrieve the data entered in the form.
        """
        data = {}
        for field in self.fields:
            column_name = field.objectName()
            data[column_name] = field.get_value()
        return data

    def validate_fields(self):
        """
        Validates the fields dynamically and highlights any empty or invalid fields with a red border.
        """
        all_valid = []
        for field in self.fields:
            all_valid.append(field.is_valid())
        
        return all(all_valid)
        
    def submit(self):
        """
        Handle form submission for both adding and editing.
        """
        try:
            form_data = self.get_form_data()
            if self.validate_fields():
                self.controller.create(**form_data)
                
                QMessageBox.information(self, "Success", "Opération effectuée avec succès.")
                self.clear_fieds()
            else:
                QMessageBox.warning(self, "Error", "Vous devez correctement renseigner tous les champs importants.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Une erreur est survenue: \n{str(e)}")
            
    def clear_fieds(self):
        for field in self.fields:
            field.clear_content()
            
    def get_cbx_items(self, column_name):
        object_list = self.controller.get_related_model_all(column_name)
        if object_list:
            return object_list
        else:
            return []
        
class CreateView(BaseFormWidget):
    refresh_data_signal = Signal()
    def __init__(self, title="", model=None, controller=None, parent=None):
        super().__init__(title, model, controller, parent)
        
    def closeEvent(self, arg__1: QCloseEvent):
        super().closeEvent(arg__1)
        self.refresh_data_signal.emit()
        
class UpdateView(BaseFormWidget):
    refresh_signal = Signal()
    def __init__(self, title="", model=None, controller=None, id=None, parent=None):
        super().__init__(title, model, controller, parent=parent)
        self.id = id  
        self.load_existing_data()

    def load_existing_data(self):
        """
        Load existing data from the database based on the primary key (id).
        """
        try:
            instance_data = self.controller.get_by_id(self.id)

            if instance_data is None:
                raise ValueError(f"No record found for the given id: {self.id}")

            for field in self.fields:
                column_name = field.objectName()
                value = getattr(instance_data, column_name)

                if isinstance(field, LabeledComboBox):
                    foreign_key = getattr(self.model.__table__.columns[column_name], 'foreign_keys', None)
                    if foreign_key:
                        related_instance = self.controller.get_related_model_item_by_id("category_id", value)
                        display_value = getattr(related_instance, 'title')  
                        field.set_value(display_value)
                    else:
                        field.set_value(str(value))
                else:
                    field.set_value(value)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Une erreur est survenue lors du chargement des données: \n{str(e)}")

    def submit(self):
        """
        Handle form submission for editing an existing record.
        """
        try:
            form_data = self.get_form_data()
            if self.validate_fields():
                self.controller.update(self.id, **form_data)  
                self.refresh_signal.emit()
                QMessageBox.information(self, "Success", "Données mises à jour avec succès.")
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Vous devez correctement renseigner tous les champs importants.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Une erreur est survenue: \n{str(e)}")
    
class ListView(QWidget):
    """
    Generic view to display list of model elements using a CustomTableWidget.
    """
    reload_data_signal = Signal()
    def __init__(self, model=None, controller=None):
        super().__init__()
        apply_stylesheet(self, theme="default_light.xml")
        self.controller = controller
        self.model = model
        self.custom_table = None
        self.setup_ui()

    def setup_ui(self):
        """
        Sets up the UI by initializing the CustomTableWidget with headers and data.
        """
        self.main_layout = QVBoxLayout()

        self.custom_table = CustomTableWidget(
            model=self.model,
            controller=self.controller,
            edit_callback=self.edit_row,
            delete_callback=self.delete_row,
            create_command=self.create_instance,
            enable_pagination=False,
            items_per_page=10
        )

        self.main_layout.addWidget(self.custom_table)
        self.setLayout(self.main_layout)

    def refresh_data(self):
        """
        Refresh the data displayed in the table.
        """
        self.custom_table.refresh_data()

    def edit_row(self, instance_id):
        """
        Edits the data of a specific row by invoking the controller.
        """
        edit_form = UpdateView(title=f"Modification d'une entrée de {self.model.__verbose_name__ if hasattr(self.model, "__verbose_name__")else self.model.__tablename__}", model=self.model, controller=self.controller, id=instance_id)
        edit_form.refresh_signal.connect(self.refresh_data)
        edit_form.exec()

    def delete_row(self, instance_id):
        """
        Handles the deletion of a database instance.

        Args:
            instance_id (int): The ID of the instance to delete.
        """
        try:
            reply = QMessageBox.question(self, "Suppression", f"Êtes-vous sûr de vouloir supprimer cette ligne de la base de données ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                response = self.controller.delete(instance_id)
                if response:
                    self.refresh_data()
                    QMessageBox.information(self, "Success", "Suppression effectuée avec succès.")
                else:
                    QMessageBox.critical(self, "Erreur", "Une erreur est survenue de la suppression de cette entrée.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Error deleting instance: {e}")
            
    def create_instance(self):
        create_form = CreateView(f"Ajouter une nouvelle entrée de {self.model.__verbose_name__ if hasattr(self.model, "__verbose_name__")else self.model.__tablename__}.", model=self.model, controller=self.controller)
        create_form.refresh_data_signal.connect(self.refresh_data)
        create_form.exec()
        
    def showEvent(self,event):
        super().showEvent(event)
        self.refresh_data()