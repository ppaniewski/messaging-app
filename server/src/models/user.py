from typing import List, TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.models.user_conversation import UserConversation
from src.models.friendship import friendships
from src.models.friend_request import friend_requests

if TYPE_CHECKING:
    from src.models.conversation import Conversation

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(nullable=False)

    user_conversations: Mapped[List["UserConversation"]] = relationship(
        "UserConversation", 
        back_populates="user",
        cascade="all, delete-orphan"
    )
    conversations: Mapped[List["Conversation"]] = relationship(
        "Conversation", secondary="user_conversations", 
        back_populates="users", viewonly=True
    )

    friend_requests_received: Mapped[List["User"]] = relationship(
        "User",
        secondary=friend_requests,
        primaryjoin=id == friend_requests.c.receiver_id,
        secondaryjoin=id == friend_requests.c.sender_id,
        back_populates="friend_requests_sent"
    )
    friend_requests_sent: Mapped[List["User"]] = relationship(
        "User",
        secondary=friend_requests,
        primaryjoin=id == friend_requests.c.sender_id,
        secondaryjoin=id == friend_requests.c.receiver_id,
        back_populates="friend_requests_received"
    )
    friends: Mapped[List["User"]] = relationship(
        "User",
        secondary=friendships,
        primaryjoin=id == friendships.c.user_id,
        secondaryjoin=id == friendships.c.friend_id
    )