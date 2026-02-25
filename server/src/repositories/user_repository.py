from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.models.user import User
from src.schemas.user_schemas import UserIn

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def commit(self):
        self.db.commit()

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_by_username(self, username: str) -> User | None:
        return self.db.query(User).where(User.username == username).first()
    
    def list(self, offset: int, limit: int | None = None) -> List[User]: 
        if limit != None:
            return self.db.query(User).order_by(User.username.asc()).limit(limit).offset(offset).all()
        
        return self.db.query(User).order_by(User.username.asc()).offset(offset).all()
    
    def list_matching_users(self, letters: str, offset: int, limit: int | None = None) -> List[User]:
        if limit != None:
            return (self.db.query(User).where(User.username.ilike(f"{letters}%")).
                    order_by(User.username.asc()).limit(limit).offset(offset).all())
        
        return (self.db.query(User).where(User.username.ilike(f"{letters}%")).
                order_by(User.username.asc()).offset(offset).all())

    def create(self, user: UserIn) -> User:
        new_user = User(username=user.username, password=user.password)
        self.db.add(new_user)
        self.db.flush()
        
        return new_user