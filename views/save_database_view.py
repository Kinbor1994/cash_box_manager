import os
import shutil
from imports import QDialog, QWidget, QVBoxLayout, QFileDialog, QMessageBox

from pyside6_custom_widgets.button import Button

from qt_material import apply_stylesheet

from utils.utils import set_app_icon
class DatabaseManager(QDialog):
    def __init__(self):
        super().__init__()
        apply_stylesheet(self, theme='default_light.xml')
        set_app_icon(self)
        self.setWindowTitle("Database Manager")
        self.setMinimumSize(300, 100)
        self.setMaximumSize(300, 100)

        layout = QVBoxLayout()

        self.backup_button = Button(text="Sauvegarder BD", icon_name="fa.save", theme_color="primary", command=self.backup_database)
        layout.addWidget(self.backup_button)

        self.restore_button = Button("Restaurer BD", icon_name="fa5s.trash-restore", theme_color="success", command=self.restore_database)
        layout.addWidget(self.restore_button)

        self.setLayout(layout)

    def backup_database(self):
        destination_folder = QFileDialog.getExistingDirectory(
            self, "Select Backup Folder", "", QFileDialog.ShowDirsOnly
        )

        if destination_folder:
            try:
                # Assure-toi que le chemin de la base de données est correct
                db_path = "database/db.db"
                backup_path = os.path.join(destination_folder, "database_backup.db")
                shutil.copy(db_path, backup_path)

                QMessageBox.information(self, "Backup Success", 
                    f"Backup completed successfully!\nLocation: {backup_path}")
            except Exception as e:
                QMessageBox.critical(self, "Backup Error", 
                    f"An error occurred during backup: {str(e)}")

    def restore_database(self):
        backup_file, _ = QFileDialog.getOpenFileName(
            self, "Selectionnez un fichier de restauration", "", "Database Files (*.db)"
        )

        if backup_file:
            try:
                # Assure-toi que le chemin de la base de données est correct
                db_path = "database/db.db"
                shutil.copy(backup_file, db_path)

                QMessageBox.information(self, "Restore Success", 
                    f"Database has been restored successfully from: {backup_file}")
            except Exception as e:
                QMessageBox.critical(self, "Restore Error", 
                    f"An error occurred during restore: {str(e)}")

if __name__ == "__main__":
    from imports import QApplication
    app = QApplication([])
    window = DatabaseManager()
    window.show()
    app.exec()
