from pathlib import Path
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL = f"sqlite:///{BASE_DIR}/db.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal  = sessionmaker(bind=engine, autocommit=False, autoflush=False)
session = SessionLocal()
Base = declarative_base()


# @contextmanager
# def get_session():
#     """
#     Gestionnaire de contexte qui fournit une session SQLAlchemy et s'assure de bien la fermer
#     après usage.
#     """
#     session = SessionLocal()
#     try:
#         yield session
#         session.commit()  
#     except:
#         session.rollback()  
#         raise