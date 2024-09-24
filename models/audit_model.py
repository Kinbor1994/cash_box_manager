from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.database import Base

from models.user import User

class AuditLog(Base):
    __tablename__ = 'audit_log'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    table_name = Column(String, nullable=False)
    action = Column(String, nullable=False)  
    record_id = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False) 
    timestamp = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    description = Column(String, nullable=False)

    user = relationship('User', back_populates='audit_logs')
    
    def __repr__(self):
        return f"<AuditLog(table={self.table_name}, action={self.action}, record_id={self.record_id}, timestamp={self.timestamp})>"
