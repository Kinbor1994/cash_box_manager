from sqlalchemy import Column, Integer, String
from database.database import Base

class Test(Base):
    """
    Model representing an income category.

    Attributes:
        id (int): The primary key identifier for the income category.
        title (str): The title or name of the income category, which must be unique and indexed.
    """
    __tablename__ = "income_categories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False, index=True)
    
  