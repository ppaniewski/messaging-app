from sqlalchemy.orm import DeclarativeBase

from src.config.database import engine

class Base(DeclarativeBase):
    pass

def init_models():
    Base.metadata.create_all(bind=engine)