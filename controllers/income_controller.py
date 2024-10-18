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

        try:
            total = session.query(func.sum(self.model.amount)).scalar()
            return total if total is not None else 0.0
        except SQLAlchemyError as e:
            raise
        finally:
            session.close()

    @property
    def get_income_by_category(self):
        try:
            income_category_data = (
                session.query(
                    IncomeCategoryModel.title.label("category"),
                    func.sum(IncomeModel.amount).label("total_amount"),
                )
                .join(IncomeModel, IncomeCategoryModel.id == IncomeModel.category_id)
                .group_by(IncomeCategoryModel.title)
                .order_by(func.sum(IncomeModel.amount).desc())
                .all()
            )
            return income_category_data
        except SQLAlchemyError as e:
            raise
        finally:
            session.close()
    
    @ property       
    def get_income_by_month(self):
        try:
            income_data = (
                session.query(
                    extract('month', IncomeModel.date).label('month'),
                    func.sum(IncomeModel.amount).label('total_income')
                )
                .group_by('month')
                .order_by('month')
                .all()
            )
            return income_data
        except SQLAlchemyError as e:
            raise 
        finally:
            session.close()


