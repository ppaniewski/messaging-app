from fastapi import Depends

from src.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository = Depends()):
        self.user_repository = user_repository

    def get_friends(self, user_id: int):
        self.user_repository.list_friends(user_id)