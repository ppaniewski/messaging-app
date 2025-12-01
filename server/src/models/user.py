from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.models.conversation import Conversation
from src.models.user_to_conversation import user_conversation
from src.models.friendship import friendships

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(nullable=False)

    conversations: Mapped[List["Conversation"]] = relationship("Conversation", secondary=user_conversation, back_populates="users")
    friends: Mapped[List["User"]] = relationship(
        "User",
        secondary=friendships,
        primaryjoin=id == friendships.c.user_id,
        secondaryjoin=id == friendships.c.friend_id
    )