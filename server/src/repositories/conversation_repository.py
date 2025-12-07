from typing import List

from fastapi import Depends
from sqlalchemy import func, distinct
from sqlalchemy.orm import Session, selectinload

from src.config.database import get_db
from src.models.conversation import Conversation
from src.models.user import User
from src.models.user_conversation import UserConversation
from src.models.message import Message

class ConversationRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def commit(self):
        self.db.commit()

    def list_conversations(self, user_id: int) -> List[Conversation]:
        return (self.db.query(Conversation).join(UserConversation).join(User)
                .options(selectinload(Conversation.users))
                .where(User.id == user_id).order_by(Conversation.id).all())
    
    def get_conversation(self, conversation_id: int) -> Conversation | None:
        return self.db.query(Conversation).where(Conversation.id == conversation_id).scalar()

    def get_conversation_by_users(self, user_ids: List[int]) -> Conversation | None:
        return (self.db.query(Conversation).join(UserConversation).join(User)
                .where(User.id._in(user_ids), Conversation.is_group_chat == False)
                .group_by(Conversation.id).having(func.count(distinct(User.id)) == len(user_ids))
                .scalar())
    
    def list_messages_from_conversations(self, conversation_ids: List[int]) -> List[Message]:
        return (self.db.query(Message).where(Message.conversation_id.in_(conversation_ids))
                .order_by(Message.conversation_id, Message.created_at.desc()).all())
    
    def get_conversation_messages(self, conversation_id: int, offset: int, amount: int) -> List[Message]:
        return (self.db.query(Message).where(Message.conversation_id == conversation_id)
                .order_by(Message.created_at.desc()).offset(offset).limit(amount).all())
    
    def create_conversation(self, user_ids: List[int], is_group_chat: bool = False) -> Conversation:
        conversation = Conversation(is_group_chat=is_group_chat)
        self.db.add(conversation)
        
        for id in user_ids:
            link = UserConversation(user_id=id, conversation_id=conversation.id)
            conversation.user_conversations.append(link)
        
        return conversation
    
    def get_message(self, message_id: int) -> Message | None:
        return self.db.query(Message).where(Message.id == message_id).scalar()
    
    def create_message(self, conversation_id: int, user_id: int, text: str) -> Message:
        message = Message(user_id=user_id, conversation_id=conversation_id, text=text)
        self.db.add(message)

        return message    