from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

class UserConversation(Base):
    __tablename__ = "user_conversations"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id"), primary_key=True)
    is_unread: Mapped[bool] = mapped_column(nullable=False, default=False)

    user = relationship("User", back_populates="user_conversations")
    conversation = relationship("Conversation", back_populates="user_conversations")