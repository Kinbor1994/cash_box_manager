from datetime import timedelta
from sqlalchemy import extract, func
from sqlalchemy.exc import SQLAlchemyError

from database.database import session
from controllers.base_controller import BaseController

from models.incomes import IncomeCategoryModel, IncomeModel


class IncomeCategoryController(BaseController):

    def __init__(self):
        super().__init__(model=IncomeCategoryModel)


class IncomeController(BaseController):

    def __init__(self):
        super().__init__(model=IncomeModel)

    @property
    def get_total_income(self):
        """
        Fetch the total income for the current period if applicable.

        Returns:
            The total income amount as a float.
        """
        try:
            current_period = self.get_current_period()
            query = session.query(func.sum(self.model.amount))

            # Filtrer par période courante si applicable
            if current_period:
                start_date = current_period.start_date
                end_date = current_period.end_date
                if self._hasattr_date():
                    query = query.filter(
                        self.model.date.between(
                            start_date, end_date + timedelta(days=1)
                        )
                    )

            total = query.scalar()
            return total if total is not None else 0.0
        except SQLAlchemyError as e:
            raise
        finally:
            session.close()

    @property
    def get_income_by_category(self):
        """
        Fetch income data grouped by category for the current period if applicable.

        Returns:
            A list of tuples with category names and their corresponding total incomes.
        """
        try:
            current_period = self.get_current_period()
            query = session.query(
                IncomeCategoryModel.title.label("category"),
                func.sum(IncomeModel.amount).label("total_amount"),
            ).join(IncomeModel, IncomeCategoryModel.id == IncomeModel.category_id)

            # Filtrer par période courante si applicable
            if current_period:
                start_date = current_period.start_date
                end_date = current_period.end_date
                if self._hasattr_date():
                    query = query.filter(
                        IncomeModel.date.between(
                            start_date, end_date + timedelta(days=1)
                        )
                    )

            income_category_data = (
                query.group_by(IncomeCategoryModel.title)
                .order_by(func.sum(IncomeModel.amount).desc())
                .all()
            )
            return income_category_data
        except SQLAlchemyError as e:
            raise
        finally:
            session.close()

    @property
    def get_income_by_month(self):
        """
        Fetch income data grouped by month for the current period if applicable.

        Returns:
            A list of tuples with month numbers and their corresponding total incomes.
        """
        try:
            current_period = self.get_current_period()
            query = session.query(
                extract("month", IncomeModel.date).label("month"),
                func.sum(IncomeModel.amount).label("total_income"),
            )

            # Filtrer par période courante si applicable
            if current_period:
                start_date = current_period.start_date
                end_date = current_period.end_date
                if self._hasattr_date():
                    query = query.filter(
                        IncomeModel.date.between(
                            start_date, end_date + timedelta(days=1)
                        )
                    )

            income_data = query.group_by("month").order_by("month").all()
            return income_data
        except SQLAlchemyError as e:
            raise
        finally:
            session.close()
