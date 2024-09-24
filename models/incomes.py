from sqlalchemy.orm import Mapped
from sqlalchemy import Column, Integer, String, Float, ForeignKey,DateTime
from sqlalchemy.orm import relationship

from database.database import Base
from models.base_model import BaseModel

class IncomeCategoryModel(BaseModel):

    __tablename__ = "income_categories"

    title = Column(String, unique=True, nullable=False, index=True, info={"verbose_name":"Title", "column_type":"text"})
    
    incomes:Mapped[list["IncomeModel"]] = relationship("IncomeModel",back_populates="category", lazy='subquery',cascade="all, delete-orphan")

    def __str__(self):
        return f"(id={self.id}, title={self.title})"
        
    def __repr__(self):
        return f"<IncomeCategoryModel(id={self.id}, title={self.title})"

class IncomeModel(BaseModel):
    
    __tablename__ = "incomes"

    amount = Column(Float, nullable=False, info={"verbose_name":"Montant", "column_type":"numeric"})
    date = Column(DateTime, nullable=False, info={"verbose_name":"Date"})
    description = Column(String, nullable=True, info={"verbose_name":"Description", "column_type":"text"})
    category_id = Column(Integer, ForeignKey("income_categories.id",ondelete="CASCADE",onupdate="CASCADE"), nullable=False, info={"verbose_name":"Catégorie"})

    category:Mapped["IncomeCategoryModel"] = relationship("IncomeCategoryModel", lazy='subquery', back_populates="incomes")
    
    def __str__(self):
        return f"(id={self.id}, amount={self.amount}, date={self.date}, description={self.description}, category={self.category.title})"
        
    def __repr__(self):
        return f"<IncomeModel(id={self.id}, amount={self.amount}, date={self.date}, description={self.description}, category_id={self.category_id})>"
    
