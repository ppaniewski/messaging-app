from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.models.user import User
from src.schemas.user_schemas import UserIn

class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_by_username(self, username: str) -> User | None:
        result = self.db.query(User).where(User.username == username).scalar()    
        return result
    
    def list(self) -> List[User]:
        return self.db.query(User).all()

    def create(self, user: UserIn) -> User:
        new_user = User(username=user.username, password=user.password)
        self.db.add(new_user)
        self.db.commit()
        return new_user
    
    def list_friends(self, user_id: int) -> List[User]:
        user = self.db.get(User, user_id)
        if user == None:
            raise Exception("Incorrect user id")
        
        return user.friends