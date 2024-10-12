from pathlib import Path

from babel.numbers import format_currency
from pyside6_custom_widgets.card import DashboardCardWidget
from pyside6_custom_widgets.charts import BarChartWidget, PieChartWidget
from pyside6_custom_widgets.dashboard import Dashboard

from imports import (
    QWidget,
    QFontDatabase,
    QVBoxLayout,
    QHBoxLayout,
    QTimer,
    Qt,
)
from utils.utils import get_initial_balance, set_app_icon
from controllers.income_controller import IncomeController
from controllers.expense_controller import ExpenseController
from views import IncomeCategoryList, IncomeList, ExpenseCategoryList, ExpenseList, ConfigForm
from qt_material import apply_stylesheet


class MainWindow(Dashboard):

    def __init__(self):
        super().__init__(menus=self.setup_menu(), sidebar_buttons=self.setup_sidebar())
        self.setWindowTitle("Gestionnaire de caisse")
        QFontDatabase.addApplicationFont("resources/fonts/Roboto-Regular.ttf")
        QFontDatabase.addApplicationFont("fonts/Lato-Regular.ttf")
        QFontDatabase.addApplicationFont("fonts/Helvetica Roman.ttf")
        apply_stylesheet(self, theme="default_light.xml")
        set_app_icon(self)
        self.setup_pages()

    def setup_menu(self):
        menus = [
            (
                "File",
                [
                    ("Fermer", self.close),
                    ("Définir Solde Initial", self.open_initial_balance_form),
                    ("Actualiser", self.refresh_dashboard),
                ],
            ),
            (
                "Révenus",
                [
                    (
                        "Catégories",
                        lambda: self.set_current_page_by_index(
                            self.get_pages_index["income_category_page_index"]
                        ),
                    ),
                    (
                        "Liste des Revenus",
                        lambda: self.set_current_page_by_index(
                            self.get_pages_index["income_page_index"]
                        ),
                    ),
                ],
            ),
            (
                "Dépenses",
                [
                    (
                        "Catégories",
                        lambda: self.set_current_page_by_index(
                            self.get_pages_index["expense_category_page_index"]
                        ),
                    ),
                    (
                        "Liste des Dépenses",
                        lambda: self.set_current_page_by_index(
                            self.get_pages_index["expense_page_index"]
                        ),
                    ),
                ],
            ),
        ]
        return menus

    def setup_sidebar(self):
        sidebar_buttons = [
            (
                "Accueil",
                "fa.home",
                lambda: self.set_current_page_by_index(
                    self.get_pages_index["main_page_index"]
                ),
            ),
            (
                "Actualiser", 
                "fa.refresh",
                self.refresh_dashboard
            ),
            (
                "Recettes",
                "fa5s.money-bill-alt",
                "",
                [
                    (
                        "Catégories",
                        "fa5s.tags",
                        lambda: self.set_current_page_by_index(
                            self.get_pages_index["income_category_page_index"]
                        ),
                    ),
                    (
                        "Liste des Revenus",
                        "fa5s.list-alt",
                        lambda: self.set_current_page_by_index(
                            self.get_pages_index["income_page_index"]
                        ),
                    ),
                ],
            ),
            (
                "Dépenses",
                "fa5s.money-bill-wave",
                "",
                [
                    (
                        "Catégories",
                        "fa5s.tags",
                        lambda: self.set_current_page_by_index(
                            self.get_pages_index["expense_category_page_index"]
                        ),
                    ),
                    (
                        "Liste des Dépenses",
                        "fa5s.list-alt",
                        lambda: self.set_current_page_by_index(
                            self.get_pages_index["expense_page_index"]
                        ),
                    ),
                ],
            ),
            (
                "Paramètres",
                "fa.cog",
                "",
                [
                    ("Fermer", "fa.close", self.close),
                    ("Actualiser", "fa.star", lambda: print("Actualisation...")),
                ],
            ),
            ("About", "fa.info-circle", lambda: print("Apropos...")),
            ("Déconnection", "fa.power-off", self.open_signin),
        ]
        return sidebar_buttons

    def open_signin(self):
        """Affiche le formulaire de connexion et cache le Dashboard."""
        from authentication.sign_in import SignIn

        self.signin_form = SignIn()
        self.signin_form.show()
        self.close()

    def open_initial_balance_form(self):
        form = ConfigForm()
        form.exec()
        
    def setup_pages(self):
        self.main_widget = self.setup_main_page()
        self.add_content_page(self.main_widget, "Analytics Dashboard")
        self.income_category_widget = IncomeCategoryList()
        self.add_content_page(
            self.income_category_widget,
            "Bienvenue sur la page des catégories des recettes",
        )
        self.income_widget = IncomeList()
        self.add_content_page(self.income_widget, "Bienvenue sur la page des recettes")
        self.expense_category_widget = ExpenseCategoryList()
        self.add_content_page(
            self.expense_category_widget,
            "Bienvenue sur la page des catégories des dépenses",
        )
        self.expense_widget = ExpenseList()
        self.add_content_page(self.expense_widget, "Bienvenue sur la page des Dépense")

    def setup_main_page(self):
        expense_controller = ExpenseController()
        total_expense = expense_controller.get_total_expense
        
        income_controller =IncomeController ()
        total_income = income_controller.get_total_income
        
        inital_balance = get_initial_balance().get("solde", "0.0")
        
        main_widget = QWidget()
        m_layout = QVBoxLayout()
        card_layout = QHBoxLayout()
        card_layout.setContentsMargins(0, 0, 0, 0)
        chart_layout = QHBoxLayout()
        chart_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setAlignment(Qt.AlignRight | Qt.AlignTop)
        
        self.initial_balance_card = DashboardCardWidget(
            title="Solde Initial",
            icon_name="fa.money",
            content=f"{format_currency(inital_balance, currency="XOF",locale='fr_FR')}",
            icon_color="blue",
        )
        self.income_card = DashboardCardWidget(
            title="Total Recette",
            icon_name="fa.money",
            content=f"{format_currency(total_income, currency="XOF",locale='fr_FR')}",
            icon_color="green",
        )
        self.expense_card = DashboardCardWidget(
            title="Total Dépense",
            icon_name="fa5s.file-invoice-dollar",
            content=f"{format_currency(total_expense, currency="XOF",locale='fr_FR')}",
            icon_color="red",
        )
        self.balance_card = DashboardCardWidget(
            title="Solde",
            icon_name="fa.money",
            content=f"{format_currency(inital_balance+total_income-total_expense, currency="XOF",locale='fr_FR')}",
            icon_color="blue",
        )
        data = IncomeController().get_all()
        bar_chart_widget = BarChartWidget(data=data, category_attr="date", value_attr="amount", title="Test", xlabel="Date", ylabel="Montant")
        chart_layout.addWidget(bar_chart_widget)
        
        pie_chart_widget = PieChartWidget(data=data, title="test", category_attr="date", value_attr="amount")
        chart_layout.addWidget(pie_chart_widget)
        
        card_layout.addWidget(self.initial_balance_card)
        card_layout.addWidget(self.income_card)
        card_layout.addWidget(self.expense_card)
        card_layout.addWidget(self.balance_card)
        m_layout.addLayout(card_layout)
        m_layout.addLayout(chart_layout)
        #m_layout.addStretch()
        main_widget.setLayout(m_layout)
        return main_widget

    def refresh_dashboard(self):
        expense_controller = ExpenseController()
        total_expense = expense_controller.get_total_expense
        
        income_controller = IncomeController()
        total_income = income_controller.get_total_income
        
        initial_balance = get_initial_balance().get("solde", "0.0")

        # Mettre à jour le contenu des widgets du tableau de bord
        self.initial_balance_card.set_content(
            f"{format_currency(initial_balance, currency='XOF', locale='fr_FR')}"
        )
        self.income_card.set_content(
            f"{format_currency(total_income, currency='XOF', locale='fr_FR')}"
        )
        self.expense_card.set_content(
            f"{format_currency(total_expense, currency='XOF', locale='fr_FR')}"
        )
        self.balance_card.set_content(
            f"{format_currency(initial_balance + total_income - total_expense, currency='XOF', locale='fr_FR')}"
        )
        
    @property
    def get_pages_index(self):
        index = {
            "main_page_index": 0,
            "income_category_page_index": 1,
            "income_page_index": 2,
            "expense_category_page_index": 3,
            "expense_page_index": 4,
        }
        return index


if __name__ == "__main__":
    import sys
    from imports import QApplication

    app = QApplication([])
    win = MainWindow()
    win.showMaximized()

    sys.exit(app.exec())
