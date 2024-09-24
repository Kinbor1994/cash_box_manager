from sqlalchemy import Date, DateTime, Float, Integer, String

from imports import QDialog, QSize, QVBoxLayout, QHBoxLayout, QFrame, QSpacerItem, QSizePolicy, QMessageBox
from pyside6_custom_widgets.button import Button
from pyside6_custom_widgets.label import Label
from pyside6_custom_widgets.labeled_combobox_2 import LabeledComboBox
from pyside6_custom_widgets.labeled_date_edit import LabeledDateEdit
from pyside6_custom_widgets.labeled_line_edit import LabeledLineEdit
from utils.utils import  set_app_icon

class BaseFormWidget(QDialog):
    
    def __init__(self, title="", model=None, controller=None, instance=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setGeometry(100,100,448, 400)
        #self.setMinimumSize(QSize(448, 400))
        #self.setMaximumSize(QSize(448, 400))
        set_app_icon(self)
        self.title = title
        self.model = model
        self.controller = controller
        self.instance = instance  
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
        Dynamically create input fields based on the model attributes.
        """
        for column in self.model.__table__.columns:
            if column.name == 'id':
                continue 
            
            field_widget = self.create_field_widget(column)
            
            if field_widget:
                field_widget.setObjectName(column.name)
                self.fields.append(field_widget)
                self.main_layout.addWidget(field_widget)

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

        if isinstance(column.type, (String, Integer, Float)) and not column.foreign_keys:
            return LabeledLineEdit(label_text=verbose_name, required=required, input_type=input_type)
        elif column.foreign_keys:
            return LabeledComboBox(label_text=verbose_name, items=self.get_cbx_items(column.name), required=required)
        elif isinstance(column.type, (Date, DateTime)):
            return LabeledDateEdit(label_text=verbose_name, required=required)

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
        all_valid = True
        for field in self.fields:
            all_valid = field.is_valid()
        
        return all_valid
        
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