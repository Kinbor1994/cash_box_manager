from sqlalchemy.orm import Mapped
from sqlalchemy import Column, Date, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.database import Base
from models import BaseModel


class IncomeCategoryModel(BaseModel):

    __tablename__ = "income_categories"
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

    incomes: Mapped[list["IncomeModel"]] = relationship(
        "IncomeModel",
        back_populates="category",
        lazy="subquery",
        cascade="all, delete-orphan",
    )

    def __str__(self):
        return f"(id={self.id}, title={self.title})"

    def __repr__(self):
        return f"<IncomeCategoryModel(id={self.id}, title={self.title})"


class IncomeModel(BaseModel):

    __tablename__ = "incomes"
    __verbose_name__ = "Recette"

    amount = Column(
        Float,
        nullable=False,
        info={"verbose_name": "Montant", "column_type": "numeric", "tab_col_index": 4},
    )
    date = Column(
        Date,
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
        ForeignKey("income_categories.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        info={
            "verbose_name": "Catégorie",
            "related_column": "title",
            "tab_col_index": 3,
        },
    )

    category: Mapped["IncomeCategoryModel"] = relationship(
        "IncomeCategoryModel", lazy="subquery", back_populates="incomes"
    )

    def __str__(self):
        return f"(id={self.id}, amount={self.amount}, date={self.date}, description={self.description}, category={self.category.title})"

    def __repr__(self):
        return f"<IncomeModel(id={self.id}, amount={self.amount}, date={self.date}, description={self.description}, category_id={self.category_id})>"
