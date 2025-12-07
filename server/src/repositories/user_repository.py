from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.models.user import User
from src.schemas.user_schemas import UserIn

class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def commit(self):
        self.db.commit()

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_by_username(self, username: str) -> User | None:
        return self.db.query(User).where(User.username == username).scalar()    
    
    def list(self) -> List[User]:
        return self.db.query(User).all()

    def create(self, user: UserIn) -> User:
        new_user = User(username=user.username, password=user.password)
        self.db.add(new_user)
        self.db.commit()
        return new_user
    
    def add_friend_request(self, user: User, friend: User):
        user.friend_requests_sent.append(friend)

    def remove_friend_request(self, user: User, friend: User):
        user.friend_requests_received.remove(friend)

    def add_friend(self, user: User, friend: User):
        user.friends.append(friend)

    def remove_friend(self, user: User, friend: User):
        user.friends.remove(friend)