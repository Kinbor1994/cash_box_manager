from sqlalchemy.orm import Mapped
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.database import Base
from models import BaseModel

class ExpenseCategoryModel(BaseModel):

    __tablename__ = "expense_categories"
    __verbose_name__ = "Catégorie"

    title = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        info={
            "verbose_name": "Titre",
            "column_type": "text",
            "order_column": True,
            "tab_col_index": 2,
        },
    )

    expenses: Mapped[list["ExpenseModel"]] = relationship(
        "ExpenseModel",
        back_populates="category",
        lazy="subquery",
        cascade="all, delete-orphan",
    )

    def __str__(self):
        return f"(id={self.id}, title={self.title})"

    def __repr__(self):
        return f"<ExpenseCategoryModel(id={self.id}, title={self.title})"
    

class ExpenseModel(BaseModel):
    __tablename__ = "expenses"
    __verbose_name__ = "Dépense"
    
    amount = Column(
        Float,
        nullable=False,
        info={"verbose_name": "Montant", "column_type": "numeric", "tab_col_index": 4},
    )
    date = Column(
        DateTime,
        nullable=False,
        info={"verbose_name": "Date", "order_column": True, "tab_col_index": 2},
    )
    description = Column(
        String(150),
        nullable=True,
        info={"verbose_name": "Description", "column_type": "text", "tab_col_index": 5},
    )
    category_id = Column(
        Integer,
        ForeignKey("expense_categories.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        info={
            "verbose_name": "Catégorie",
            "related_column": "title",
            "tab_col_index": 3,
        },
    )

    category: Mapped["ExpenseCategoryModel"] = relationship(
        "ExpenseCategoryModel", lazy="subquery", back_populates="expenses"
    )

    def __str__(self):
        return f"(id={self.id}, amount={self.amount}, date={self.date}, description={self.description}, category={self.category.title})"

    def __repr__(self):
        return f"<IncomeModel(id={self.id}, amount={self.amount}, date={self.date}, description={self.description}, category_id={self.category_id})>"