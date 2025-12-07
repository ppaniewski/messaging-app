from typing import List, TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.models.user_conversation import UserConversation

if TYPE_CHECKING:
    from src.models.user import User
    from src.models.message import Message

class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(primary_key=True)
    is_group_chat: Mapped[bool] = mapped_column(nullable=False, default=False)
    name: Mapped[str | None] = mapped_column()
    
    user_conversations: Mapped[List["UserConversation"]] = relationship("UserConversation", back_populates="conversation")
    users: Mapped[List["User"]] = relationship(
        "User", secondary="user_conversations", 
        back_populates="conversations", viewonly=True
    )

    messages: Mapped[List["Message"]] = relationship("Message", back_populates="conversation")