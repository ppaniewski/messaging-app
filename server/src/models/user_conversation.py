from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.user import User
    from src.models.conversation import Conversation

class UserConversation(Base):
    __tablename__ = "user_conversations"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id"), primary_key=True)
    is_unread: Mapped[bool] = mapped_column(nullable=False, default=False)

    user: Mapped["User"] = relationship("User", back_populates="user_conversations")
    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="user_conversations")