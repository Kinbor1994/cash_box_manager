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

        try:
            total = session.query(func.sum(self.model.amount)).scalar()
            return total if total is not None else 0.0
        except SQLAlchemyError as e:
            raise
        finally:
            session.close()

    @property
    def get_expense_by_category(self):
        try:
            expense_category_data = (
                session.query(
                    ExpenseCategoryModel.title.label("category"),
                    func.sum(ExpenseModel.amount).label("total_amount"),
                )
                .join(ExpenseModel, ExpenseCategoryModel.id == ExpenseModel.category_id)
                .group_by(ExpenseCategoryModel.title)
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
        try:
            expense_data = (
                session.query(
                    extract('month', ExpenseModel.date).label('month'),
                    func.sum(ExpenseModel.amount).label('total_expense')
                )
                .group_by('month')
                .order_by('month')
                .all()
            )
            return expense_data
        except Exception as e:
            raise
        finally:
            session.close()
