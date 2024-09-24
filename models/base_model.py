from sqlalchemy import Column, Integer, DateTime, func
from database.database import Base

class BaseModel(Base):
    """
    Generic model that provides common attributes for all derived models.
    Includes 'id', 'created_at', and 'updated_at' columns.
    """

    __abstract__ = True  # Mark this class as abstract so it won't be mapped to a table

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=func.now(), nullable=False, info={"editable":"false"})
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False, info={"editable":"false"})

