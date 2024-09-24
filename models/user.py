from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    secret_question = Column(String, nullable=False)  
    secret_answer = Column(String, nullable=False)    
    
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")