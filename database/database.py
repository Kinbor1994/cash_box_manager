from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL = f"sqlite:///{BASE_DIR}/db.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal  = sessionmaker(bind=engine, autocommit=False, autoflush=False)
session = SessionLocal()
Base = declarative_base()
