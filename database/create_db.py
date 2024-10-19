from pathlib import Path
from database.database import Base, engine, DB_DIR
from models.user import User
from models.audit_model import AuditLog
from models import IncomeCategoryModel, IncomeModel, ExpenseCategoryModel, ExpenseModel, CashBoxPeriod

def check_and_create_db():
    """Checks if the database exists; if not, creates it.
    """
    db_file_path = DB_DIR / 'db.db'
    
    if not db_file_path.exists():
        try:
            Base.metadata.create_all(bind=engine)
        except Exception as e:
            print(f"Error occurred while creating the database: {e}")    
            
