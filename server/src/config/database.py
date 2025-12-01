import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = f"{os.getenv("DATABASE_URL")}"

engine = create_engine(
    DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=True
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()