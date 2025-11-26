from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from src.models.base import Base
from src.models.user_to_conversation import user_conversation

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    
    users = relationship("User", secondary=user_conversation, back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")