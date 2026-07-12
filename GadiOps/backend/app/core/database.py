import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite configuration (stored locally in the backend directory)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./gadiops.db")

# connect_args={"check_same_thread": False} is required exclusively for SQLite
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get DB session in routers
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()