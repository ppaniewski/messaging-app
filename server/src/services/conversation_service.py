from typing import List

from fastapi import Depends

from src.repositories.conversation_repository import ConversationRepository
from src.repositories.user_repository import UserRepository
from src.models.user import User
from src.exceptions.exceptions import NotFoundException, BadRequestException, ServerErrorException
from src.schemas.conversation_schemas import MessageOut, ConversationOut, UserOut

class ConversationService:
    def __init__(
            self, 
            conversation_repository: ConversationRepository = Depends(), 
            user_repository: UserRepository = Depends()
    ):
        self.conversation_repository = conversation_repository
        self.user_repository = user_repository

    def get_conversations(self, user_id: int, message_limit: int) -> List[ConversationOut]:
        # Get the user's conversations sorted by their id
        conversations = self.conversation_repository.list_conversations(user_id)
        conversation_ids = [c.id for c in conversations]

        # Get all the messages from the user's conversations sorted by conversation id
        messages = self.conversation_repository.list_messages_from_conversations(conversation_ids)

        message_lists = [[] for i in range(len(conversations))]
        conversation_index = 0
        message_count = 0
        for m in messages:
            for i in range(conversation_index, len(conversation_ids)):
                id = conversations[i].id

                if m.conversation_id != id or message_count >= message_limit:
                    conversation_index += 1
                    message_count = 0
                    continue

                message_lists[i].append(MessageOut(
                    text=m.text, id=m.id, user_id=m.user_id, 
                    is_deleted=m.is_deleted, created_at=m.created_at
                ))
                message_count += 1
                
        user_lists = [[] for i in range(len(conversations))]
        for i in range(len(conversations)):
            conversation = conversations[i]
            for user in conversation.users:
                user_lists[i].append(UserOut(id=user.id, username=user.username))

        conversations_out = []
        for i in range(len(conversations)):
            c = conversations[i]
            conversations_out.append(ConversationOut(
                id=c.id, is_group_chat=c.is_group_chat, name=c.name, 
                messages=message_lists[i], users=user_lists[i]
            ))

        return conversations_out
    
    def get_conversation_messages(self, user_id: int, conversation_id: int, offset: int, amount: int) -> List[MessageOut]:
        conversation = self.conversation_repository.get_conversation(conversation_id)
        if conversation == None:
            raise NotFoundException("Conversation not found")
        
        messages = self.conversation_repository.get_conversation_messages(conversation_id, offset, amount)
        messages_out = [MessageOut(text=m.text, id=m.id, user_id=m.user_id, 
                                   is_deleted=m.is_deleted, created_at=m.created_at) for m in messages]
        
        return messages_out

    def send_user_message(self, recipient_username: str, user_id: int, text: str) -> MessageOut:
        user = self.__get_user_by_id(user_id)
        recipient = self.__get_user_by_username(recipient_username)

        if user == recipient:
            raise BadRequestException("User can't send message to himself")
        
        conversation = self.conversation_repository.get_conversation_by_users([user.id, recipient.id])
        if conversation == None:
            conversation = self.conversation_repository.create_conversation([user.id, recipient.id], False)
        
        message = self.conversation_repository.create_message(conversation.id, user.id, text)
        self.conversation_repository.commit()

        return MessageOut(text=message.text, id=message.id, user_id=user_id, 
                          is_deleted=message.is_deleted, created_at=message.created_at)
    
    def delete_user_message(self, user_id: int, message_id: int) -> MessageOut:
        user = self.__get_user_by_id(user_id)
        
        message = self.conversation_repository.get_message(message_id)
        if message == None:
            raise NotFoundException("Message not found")
        
        if user.id != message.user_id:
            raise BadRequestException("Can't access another user's message")
        
        deleted_text_replacement = "X"
        message.is_deleted = True
        message.text = deleted_text_replacement

        self.conversation_repository.commit()

        return MessageOut(text=message.text, id=message.id, is_deleted=True, user_id=user_id, created_at=message.created_at)

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