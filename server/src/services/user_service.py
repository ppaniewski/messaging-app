from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from src.repositories.user_repository import UserRepository
from src.repositories.conversation_repository import ConversationRepository
from src.exceptions.exceptions import NotFoundException, BadRequestException
from src.models.user import User
from src.schemas.user_schemas import UserOut

class UserService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
        self.conversation_repo = ConversationRepository(db)

    def get_users(
        self, username_string: str | None = None,
        limit: int | None = None, offset: int | None = None
    ) -> List[UserOut]:
        if offset == None:
            offset = 0

        if username_string == None:
            users = self.user_repo.list(offset, limit)
        else:
            users = self.user_repo.list_matching_users(username_string, offset, limit)
        
        return [UserOut(username=user.username, id=user.id) for user in users]

    def get_friends(self, user_id: int) -> List[UserOut]:
        user = self.user_repo.get_by_id(user_id)
        if user == None:
            raise NotFoundException("User not found")

        friends = user.friends
        return [UserOut(username=friend.username, id=friend.id) for friend in friends]
    
    def send_friend_request(self, friend_id: int, user_id: int):
        user = self._get_user_by_id(user_id)
        friend = self._get_user_by_id(friend_id)
        
        if user_id == friend_id:
            raise BadRequestException("User can't befriend himself")

        if any(friend.id == f.id for f in user.friends):
            raise BadRequestException("Provided user is already a friend")
        if any(user.id == u.id for u in friend.friend_requests_sent):
            raise BadRequestException("There is an existing friend request from the other user")
        if any(user.id == u.id for u in friend.friend_requests_received):
            raise BadRequestException("Friend request is already sent")
        
        user.friend_requests_sent.append(friend)
        self.user_repo.commit()
    
    def accept_friend_request(self, friend_id: int, user_id: int):
        user = self._get_user_by_id(user_id)    
        friend = self._get_user_by_id(friend_id)
        
        if user_id == friend_id:
            raise BadRequestException("User can't befriend himself")
        
        if not any(friend_id == u.id for u in user.friend_requests_received):
            raise BadRequestException("No friend request received from this user")
        
        # Remove friend request
        self._pop_user_by_id(friend_id, user.friend_requests_received)

        user.friends.append(friend)
        friend.friends.append(user)

        # Create empty conversation between users if one doesn't already exist
        existing_convo = self.conversation_repo.get_conversation_by_users([user_id, friend_id])
        if existing_convo == None:
            new_convo = self.conversation_repo.create_conversation([user_id, friend_id])

        self.conversation_repo.commit()
        self.user_repo.commit()
    
    def decline_friend_request(self, friend_id: int, user_id: int):
        user = self._get_user_by_id(user_id)
        
        if user_id == friend_id:
            raise BadRequestException("User can't befriend himself")
        
        if not any(friend_id == u.id for u in user.friend_requests_received):
            raise BadRequestException("No friend request received from this userr")
        
        # Remove friend request
        self._pop_user_by_id(friend_id, user.friend_requests_received)

        self.user_repo.commit()

    def remove_friend(self, friend_id: int, user_id: int):
        user = self._get_user_by_id(user_id)
        friend = self._get_user_by_id(friend_id)

        if user == friend:
            raise BadRequestException("User can't befriend himself")
        
        if friend not in user.friends:
            raise BadRequestException("User is not a friend")
        
        self._pop_user_by_id(friend_id, user.friends)
        self._pop_user_by_id(user_id, friend.friends)

        # If there's an empty conversation between the two users, delete it
        existing_convo = self.conversation_repo.get_conversation_by_users([user_id, friend_id])
        if existing_convo and len(existing_convo.messages) == 0:
            self.conversation_repo.delete_conversation(existing_convo)
        
        self.conversation_repo.commit()
        self.user_repo.commit()
    
    def get_sent_friend_requests(self, user_id: int) -> List[UserOut]:
        user = self.user_repo.get_by_id(user_id)
        if user == None:
            raise NotFoundException("User not found")
        
        return [UserOut(id=user.id, username=user.username) for user in user.friend_requests_sent]
    
    def get_received_friend_requests(self, user_id: int) -> List[UserOut]:
        user = self.user_repo.get_by_id(user_id)
        if user == None:
            raise NotFoundException("User not found")
        
        return [UserOut(id=user.id,username=user.username) for user in user.friend_requests_received]
    
    def get_user(self, user_id: int) -> UserOut:
        user = self._get_user_by_id(user_id)
        return UserOut(id=user.id, username=user.username)
    
    def _pop_user_by_id(self, user_id: int, user_list: list):
        for i, u in enumerate(user_list):
            if u.id == user_id:
                user_list.pop(i)
                return
    
    def _get_user_by_id(self, id: int) -> User:
        user = self.user_repo.get_by_id(id)
        if user == None:
            raise NotFoundException("User not found")
        
        return user