from typing import List

from fastapi import Depends

from src.repositories.user_repository import UserRepository
from src.exceptions.exceptions import NotFoundException, BadRequestException
from src.models.user import User
from src.schemas.user_schemas import UserOut

class UserService:
    def __init__(self, user_repository: UserRepository = Depends()):
        self.user_repository = user_repository

    def get_users(self) -> List[UserOut]:
        users = self.user_repository.list()
        return [UserOut(username=user.username, id=user.id) for user in users]

    def get_friends(self, user_id: int) -> List[UserOut]:
        user = self.user_repository.get_by_id(user_id)
        if user == None:
            raise NotFoundException("User not found")

        friends = user.friends
        return [UserOut(username=friend.username, id=friend.id) for friend in friends]
    
    def send_friend_request(self, friend_username: str, user_id: int):
        user = self.__get_user_by_id(user_id)
        friend = self.__get_user_by_username(friend_username)
        
        if user == friend:
            raise BadRequestException("User can't befriend himself")

        if friend in user.friends:
            raise BadRequestException("Provided user is already a friend")
        if user in friend.friend_requests_received or friend in user.friend_requests_sent:
            raise BadRequestException("Friend request already is sent")
        
        self.user_repository.add_friend_request(user, friend)
        self.user_repository.commit()
    
    def accept_friend_request(self, friend_username: str, user_id: int):
        user = self.__get_user_by_id(user_id)    
        friend = self.__get_user_by_username(friend_username)
        
        if user == friend:
            raise BadRequestException("User can't befriend himself")
        
        if friend not in user.friend_requests_received:
            raise BadRequestException("No friend request received from this user")
        
        self.user_repository.remove_friend_request(user, friend)
        self.user_repository.add_friend(user, friend)
        self.user_repository.add_friend(friend, user)

        self.user_repository.commit()
    
    def decline_friend_request(self, friend_username: str, user_id: int):
        user = self.__get_user_by_id(user_id)
        friend = self.__get_user_by_username(friend_username)
        
        if user == friend:
            raise BadRequestException("User can't befriend himself")
        
        if friend not in user.friend_requests_received:
            raise BadRequestException("No friend request received from this userr")
        
        self.user_repository.remove_friend_request(user, friend)
        self.user_repository.commit()

    def remove_friend(self, friend_username: str, user_id: int):
        user = self.__get_user_by_id(user_id)
        friend = self.__get_user_by_username(friend_username)

        if user == friend:
            raise BadRequestException("User can't befriend himself")
        
        if friend not in user.friends:
            raise BadRequestException("User is not a friend")
        
        self.user_repository.remove_friend(user, friend)
        self.user_repository.commit()
    
    def get_sent_friend_requests(self, user_id: int) -> List[UserOut]:
        user = self.user_repository.get_by_id(user_id)
        if user == None:
            raise NotFoundException("User not found")
        
        return [UserOut(id=user.id, username=user.username) for user in user.friend_requests_sent]
    
    def get_received_friend_requests(self, user_id: int) -> List[UserOut]:
        user = self.user_repository.get_by_id(user_id)
        if user == None:
            raise NotFoundException("User not found")
        
        return [UserOut(id=user.id,username=user.username) for user in user.friend_requests_received]
    
    def __get_user_by_id(self, id: int) -> User:
        user = self.user_repository.get_by_id(id)
        if user == None:
            raise NotFoundException("User not found")
        
        return user
    
    def __get_user_by_username(self, username: str) -> User:
        user = self.user_repository.get_by_username(username)
        if user == None:
            raise NotFoundException("User not found")
        
        return user