from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.models.user import User
from src.models.message import Message
from src.models.user_to_conversation import user_conversation

class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    users: Mapped[List["User"]] = relationship("User", secondary=user_conversation, back_populates="conversations")
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="conversation")