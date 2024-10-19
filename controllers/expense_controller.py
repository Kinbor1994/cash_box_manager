from datetime import timedelta
from sqlalchemy import extract, func
from sqlalchemy.exc import SQLAlchemyError

from database.database import session
from controllers import BaseController

from models import ExpenseCategoryModel, ExpenseModel


class ExpenseCategoryController(BaseController):

    def __init__(self):
        super().__init__(model=ExpenseCategoryModel)


class ExpenseController(BaseController):

    def __init__(self):
        super().__init__(model=ExpenseModel)

    @property
    def get_total_expense(self):
        """
        Fetch the total expense for the current period if applicable.

        Returns:
            The total expense amount as a float.
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
    def get_expense_by_category(self):
        """
        Fetch expense data grouped by category for the current period if applicable.

        Returns:
            A list of tuples with category names and their corresponding total expenses.
        """
        try:
            current_period = self.get_current_period()
            query = session.query(
                ExpenseCategoryModel.title.label("category"),
                func.sum(ExpenseModel.amount).label("total_amount"),
            ).join(ExpenseModel, ExpenseCategoryModel.id == ExpenseModel.category_id)

            # Filtrer par période courante si applicable
            if current_period:
                start_date = current_period.start_date
                end_date = current_period.end_date
                if self._hasattr_date():
                    query = query.filter(
                        ExpenseModel.date.between(
                            start_date, end_date + timedelta(days=1)
                        )
                    )

            expense_category_data = (
                query.group_by(ExpenseCategoryModel.title)
                .order_by(func.sum(ExpenseModel.amount).desc())
                .all()
            )
            return expense_category_data
        except SQLAlchemyError as e:
            raise
        finally:
            session.close()

    @property
    def get_expense_by_month(self):
        """
        Fetch expense data grouped by month for the current period if applicable.

        Returns:
            A list of tuples with month numbers and their corresponding total expenses.
        """
        try:
            current_period = self.get_current_period()
            query = session.query(
                extract("month", ExpenseModel.date).label("month"),
                func.sum(ExpenseModel.amount).label("total_expense"),
            )

            # Filtrer par période courante si applicable
            if current_period:
                start_date = current_period.start_date
                end_date = current_period.end_date
                if self._hasattr_date():
                    query = query.filter(
                        ExpenseModel.date.between(
                            start_date, end_date + timedelta(days=1)
                        )
                    )

            expense_data = query.group_by("month").order_by("month").all()
            return expense_data
        except SQLAlchemyError as e:
            raise
        finally:
            session.close()
