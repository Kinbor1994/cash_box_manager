from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout
)
from PySide6.QtCore import Qt, QSortFilterProxyModel
from PySide6.QtGui import QStandardItemModel, QStandardItem

class MultiFilterTable(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre principale
        self.setWindowTitle("Multi-Column Filter Table")
        self.setGeometry(100, 100, 800, 600)

        # Création du modèle de données de la table
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Name', 'Age', 'City'])

        # Remplir le modèle avec des données d'exemple
        data = [
            ['Alice', '30', 'New York'],
            ['Bob', '25', 'Los Angeles'],
            ['Charlie', '35', 'Chicago'],
            ['David', '40', 'San Francisco'],
            ['Eva', '29', 'Houston'],
        ]
        for row in data:
            items = [QStandardItem(field) for field in row]
            self.model.appendRow(items)

        # Configuration du QSortFilterProxyModel pour gérer le filtrage
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterKeyColumn(-1)  # Filtrage sur toutes les colonnes

        # Création du QTableView et application du modèle proxy
        self.table_view = QTableView()
        self.table_view.setModel(self.proxy_model)

        # Création de champs de filtrage pour chaque colonne
        self.filter_layout = QHBoxLayout()
        self.filters = []

        for column in range(self.model.columnCount()):
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(f'Filter {self.model.headerData(column, Qt.Horizontal)}')
            line_edit.textChanged.connect(self.create_filter_function(column))
            self.filter_layout.addWidget(line_edit)
            self.filters.append(line_edit)

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.filter_layout)
        main_layout.addWidget(self.table_view)

        # Création du conteneur principal
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def create_filter_function(self, column):
        """Crée une fonction de filtrage pour une colonne spécifique."""
        def filter_text(text):
            # Appliquer le filtre à la colonne donnée
            pattern = f".*{text}.*"
            self.proxy_model.setFilterRegularExpression(pattern)
            self.proxy_model.setFilterKeyColumn(column)

        return filter_text

if __name__ == '__main__':
    app = QApplication([])
    window = MultiFilterTable()
    window.show()
    app.exec()
