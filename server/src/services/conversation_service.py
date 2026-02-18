from typing import List
from collections import defaultdict

from fastapi import Depends
from sqlalchemy.orm import Session

from src.repositories.conversation_repository import ConversationRepository
from src.repositories.user_repository import UserRepository
from src.models.user import User
from src.exceptions.exceptions import NotFoundException, BadRequestException
from src.schemas.conversation_schemas import MessageOut, MessageOutExtended, ConversationOut, UserOutConversation

class ConversationService:
    def __init__(self, db: Session):
        self.conversation_repository = ConversationRepository(db)
        self.user_repository = UserRepository(db)

    def get_conversations(
        self, user_id: int, message_limit: int,
        limit: int | None = None, offset: int | None = None
    ) -> List[ConversationOut]:
        if offset == None:
            offset = 0

        # Get the user's conversations sorted by their id
        conversations = self.conversation_repository.list_conversations(user_id, offset, limit)
        conversation_ids = [c.id for c in conversations]

        # Get all the messages from the user's conversations sorted by conversation id
        messages = self.conversation_repository.list_messages_from_conversations(conversation_ids)

        # Group messages by conversation
        messages_by_conversation = defaultdict(list)
        for m in messages:
            messages_by_conversation[m.conversation_id].append(MessageOut(
                text=m.text,
                id=m.id,
                user_id=m.user_id,
                is_deleted=m.is_deleted,
                created_at=m.created_at
            ))

        message_lists = [[] for _ in conversations]
        for i, c in enumerate(conversations):
            message_lists[i] = messages_by_conversation[c.id][:message_limit]
                
        user_lists = [[] for _ in conversations]
        for i, c in enumerate(conversations):
            for link in c.user_conversations:
                u = link.user
                user_lists[i].append(UserOutConversation(id=u.id, username=u.username, is_unread=link.is_unread))

        conversations_out = []
        for i, c in enumerate(conversations):
            conversations_out.append(ConversationOut(
                id=c.id, is_group_chat=c.is_group_chat, name=c.name, 
                messages=message_lists[i], users=user_lists[i]
            ))

        return conversations_out
    
    def get_conversation(self, conversation_id: int) -> ConversationOut:
        conversation = self.conversation_repository.get_conversation(conversation_id)
        if conversation == None:
            raise NotFoundException("Conversation not found")
        
        messages_out = [
            MessageOut(
                text=m.text, id=m.id, user_id=m.user_id, 
                is_deleted=m.is_deleted, created_at=m.created_at
            ) for m in conversation.messages]
        
        users_out = []
        for link in conversation.user_conversations:
            u = link.user
            users_out.append(UserOutConversation(id=u.id,username=u.username, is_unread=link.is_unread))
        
        return ConversationOut(
            id=conversation.id,
            is_group_chat=conversation.is_group_chat,
            name=conversation.name,
            messages=messages_out,
            users=users_out
        )
    
    def get_conversation_messages(self, user_id: int, conversation_id: int, offset: int, amount: int) -> List[MessageOut]:
        conversation = self.conversation_repository.get_conversation(conversation_id)
        if conversation == None:
            raise NotFoundException("Conversation not found")
        
        messages = self.conversation_repository.get_conversation_messages(conversation_id, offset, amount)
        messages_out = [MessageOut(text=m.text, id=m.id, user_id=m.user_id, 
                                   is_deleted=m.is_deleted, created_at=m.created_at) for m in messages]
        
        return messages_out

    def send_user_message(self, recipient_id: int, user_id: int, text: str) -> MessageOutExtended:
        if user_id == recipient_id:
            raise BadRequestException("User can't send message to himself")
        
        conversation = self.conversation_repository.get_conversation_by_users([user_id, recipient_id])
        if conversation == None:
            conversation = self.conversation_repository.create_conversation([user_id, recipient_id], False)
        
        message = self.conversation_repository.create_message(conversation.id, user_id, text)

        # Mark the conversation as unread for the recipient
        user_conversations = conversation.user_conversations
        for link in user_conversations:
            if link.user_id == user_id:
                continue
        
            link.is_unread = True
            
        self.conversation_repository.commit()

        return MessageOutExtended(
            text=message.text, id=message.id, user_id=user_id, conversation_id=conversation.id,
            is_deleted=message.is_deleted, created_at=message.created_at
        )
    
    def delete_user_message(self, user_id: int, message_id: int) -> MessageOutExtended:
        message = self.conversation_repository.get_message(message_id)
        if message == None:
            raise NotFoundException("Message not found")
        
        if user_id != message.user_id:
            raise BadRequestException("Can't access another user's message")
        
        deleted_text_replacement = ""
        message.is_deleted = True
        message.text = deleted_text_replacement

        self.conversation_repository.commit()

        return MessageOutExtended(
            text=message.text, id=message.id, conversation_id=message.conversation_id,
            is_deleted=True, user_id=user_id, created_at=message.created_at
        )
    
    def mark_conversation_read(self, user_id: int, conversation_id: int) -> None:
        conversation = self.conversation_repository.get_conversation(conversation_id)
        if conversation == None:
            raise NotFoundException("Conversation not found")
        
        if not any(u.id == user_id for u in conversation.users):
            raise BadRequestException("User is not part of the conversation")
        
        for link in conversation.user_conversations:
            if link.user.id != user_id:
                continue

            link.is_unread = False

        self.conversation_repository.commit()