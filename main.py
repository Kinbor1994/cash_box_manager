from babel.numbers import format_currency

from controllers.cash_box_controller import CashBoxPeriodController
from pyside6_custom_widgets.card import DashboardCardWidget
from pyside6_custom_widgets.charts import (
    BarChartWidgetWithTwoDataSets,
    PieChartWidget,
)
from pyside6_custom_widgets.dashboard import Dashboard

from imports import (
    QWidget,
    QFontDatabase,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    Qt,
)
from utils.utils import  set_app_icon
from controllers.income_controller import IncomeController
from controllers.expense_controller import ExpenseController
from views import (
    IncomeCategoryList,
    IncomeList,
    ExpenseCategoryList,
    ExpenseList,
)
from qt_material import apply_stylesheet

from views.about_us import AboutUs
from views.manage_periodes_views import CashBoxPeriodList
from views.save_database_view import DatabaseManager


class MainWindow(Dashboard):

    def __init__(self):
        super().__init__(menus=self.setup_menu(), sidebar_buttons=self.setup_sidebar())
        self.setWindowTitle("CASH BOX MANAGER BY BOREL")
        QFontDatabase.addApplicationFont("resources/fonts/Roboto-Regular.ttf")
        QFontDatabase.addApplicationFont("fonts/Lato-Regular.ttf")
        QFontDatabase.addApplicationFont("fonts/Helvetica Roman.ttf")
        apply_stylesheet(self, theme="default_light.xml")
        set_app_icon(self)
        self.income_controller = IncomeController()
        self.expense_controller = ExpenseController()
        self.cash_box_perid_controller =  CashBoxPeriodController()
        self.setup_pages()

    def setup_menu(self):
        menus = [
            (
                "File",
                [
                    ("Fermer", self.close),
                    ("Actualiser", self.refresh_dashboard),
                    ("Sauvegarder/Restaurer", self.show_db_manager)
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
            ("Actualiser", "fa.refresh", self.refresh_dashboard),
            (
                "Exercices",
                "fa5s.calendar",
                "",
                [
                    (
                        "Liste des exercices",
                        "fa5s.list-alt",
                        lambda: self.set_current_page_by_index(
                            self.get_pages_index["cash_box_period_page_index"]
                        ),
                    ),
                ],
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
            ("About", "fa.info-circle", self.show_about_us),
            ("Déconnection", "fa.power-off", self.open_signin),
        ]
        return sidebar_buttons

    def open_signin(self):
        """Affiche le formulaire de connexion et cache le Dashboard."""
        from authentication.sign_in import SignIn

        self.signin_form = SignIn()
        self.signin_form.show()
        self.close()

    def setup_pages(self):
        current_period = self.cash_box_perid_controller.get_current_period()
        self.main_widget = self.setup_main_page()
        self.add_content_page(self.main_widget, f"Analytics Dashboard - (Exercice du {current_period.start_date.strftime("%d/%m/%Y") if current_period else "--/--/----"} au {current_period.end_date.strftime("%d/%m/%Y") if current_period else "--/--/----"})")
        self.cash_box_period_widget = CashBoxPeriodList()
        self.add_content_page(
            self.cash_box_period_widget,
            "Bienvenue sur la page d'ouverture et de fermeture d'un exercice.",
        )
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
        total_expense = self.expense_controller.get_total_expense
        total_income = self.income_controller.get_total_income

        inital_balance = self.cash_box_perid_controller.get_initial_balance

        main_widget = QWidget()
        self.page_scroll_area = QScrollArea()
        self.page_scroll_area.setWidgetResizable(True)
        self.page_scroll_area.setWidget(main_widget)
        m_layout = QVBoxLayout()
        card_layout = QHBoxLayout()
        card_layout.setContentsMargins(0, 0, 0, 0)
        chart_layout = QHBoxLayout()
        chart_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        chart_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

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
            icon_name="fa.money",
            content=f"{format_currency(total_expense, currency="XOF",locale='fr_FR')}",
            icon_color="red",
        )
        self.balance_card = DashboardCardWidget(
            title="Solde",
            icon_name="fa.money",
            content=f"{format_currency(inital_balance+total_income-total_expense, currency="XOF",locale='fr_FR')}",
            icon_color="blue",
        )
        income_data = self.income_controller.get_income_by_category
        income_monthly_data = self.income_controller.get_income_by_month
        expense_data = self.expense_controller.get_expense_by_category
        expense_monthly_data = self.expense_controller.get_expense_by_month

        self.income_pie_chart_widget = PieChartWidget(data=income_data, title="Revenus par catégorie")
        self.income_pie_chart_widget.setMinimumSize(350, 350)
        chart_layout.addWidget(self.income_pie_chart_widget)

        self.expense_pie_chart_widget = PieChartWidget(data=expense_data, title="Dépenses par catégorie")
        self.expense_pie_chart_widget.setMinimumSize(350, 350)
        chart_layout.addWidget(self.expense_pie_chart_widget)

        income_vs_expense_bar_chart_layout = QHBoxLayout()
        self.income_vs_expense_bar_chart = BarChartWidgetWithTwoDataSets(
            income_data=income_monthly_data,
            expense_data=expense_monthly_data,
            title="Evolution mensuelle des revenus et des dépenses",
            xlabel="Mois",
            ylabel="Montant",
        )
        self.income_vs_expense_bar_chart.setMinimumSize(350, 400)
        income_vs_expense_bar_chart_layout.addWidget(self.income_vs_expense_bar_chart)

        card_layout.addWidget(self.initial_balance_card)
        card_layout.addWidget(self.income_card)
        card_layout.addWidget(self.expense_card)
        card_layout.addWidget(self.balance_card)
        m_layout.addLayout(card_layout)
        m_layout.addLayout(chart_layout)
        m_layout.addLayout(income_vs_expense_bar_chart_layout)
        m_layout.addStretch()
        main_widget.setLayout(m_layout)
        return self.page_scroll_area

    def refresh_dashboard(self):
        expense_controller = ExpenseController()
        total_expense = expense_controller.get_total_expense

        income_controller = IncomeController()
        total_income = income_controller.get_total_income

        initial_balance = self.cash_box_perid_controller.get_initial_balance

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

        income_data = self.income_controller.get_income_by_category
        income_monthly_data = self.income_controller.get_income_by_month
        expense_data = self.expense_controller.get_expense_by_category
        expense_monthly_data = self.expense_controller.get_expense_by_month

        self.income_pie_chart_widget.update_chart(income_data)
        self.expense_pie_chart_widget.update_chart(expense_data)
        self.income_vs_expense_bar_chart.update_chart(
            new_income_data=income_monthly_data, new_expense_data=expense_monthly_data
        )

    def show_about_us(self):
        form = AboutUs()
        form.exec()
        
    def show_db_manager(self):
        form = DatabaseManager()
        form.exec()
        
    @property
    def get_pages_index(self):
        index = {
            "main_page_index": 0,
            "cash_box_period_page_index":1,
            "income_category_page_index": 2,
            "income_page_index": 3,
            "expense_category_page_index": 4,
            "expense_page_index": 5,
        }
        return index


if __name__ == "__main__":
    import sys
    from imports import QApplication

    app = QApplication([])
    win = MainWindow()
    win.showMaximized()

    sys.exit(app.exec())
