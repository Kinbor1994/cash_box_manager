import os
import shutil
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox
)

class DatabaseManager(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Database Manager")
        self.resize(400, 150)

        layout = QVBoxLayout()

        self.backup_button = QPushButton("Backup Database")
        self.backup_button.clicked.connect(self.backup_database)
        layout.addWidget(self.backup_button)

        self.restore_button = QPushButton("Restore Database")
        self.restore_button.clicked.connect(self.restore_database)
        layout.addWidget(self.restore_button)

        self.setLayout(layout)

    def backup_database(self):
        destination_folder = QFileDialog.getExistingDirectory(
            self, "Select Backup Folder", "", QFileDialog.ShowDirsOnly
        )

        if destination_folder:
            try:
                # Assure-toi que le chemin de la base de données est correct
                db_path = "db.db"
                backup_path = os.path.join(destination_folder, "database_backup.db")
                shutil.copy(db_path, backup_path)

                QMessageBox.information(self, "Backup Success", 
                    f"Backup completed successfully!\nLocation: {backup_path}")
            except Exception as e:
                QMessageBox.critical(self, "Backup Error", 
                    f"An error occurred during backup: {str(e)}")

    def restore_database(self):
        backup_file, _ = QFileDialog.getOpenFileName(
            self, "Select Backup File", "", "Database Files (*.db)"
        )

        if backup_file:
            try:
                # Assure-toi que le chemin de la base de données est correct
                db_path = "db.db"
                shutil.copy(backup_file, db_path)

                QMessageBox.information(self, "Restore Success", 
                    f"Database has been restored successfully from: {backup_file}")
            except Exception as e:
                QMessageBox.critical(self, "Restore Error", 
                    f"An error occurred during restore: {str(e)}")

if __name__ == "__main__":
    app = QApplication([])
    window = DatabaseManager()
    window.show()
    app.exec()
