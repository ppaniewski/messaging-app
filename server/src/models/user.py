from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.models.base import Base
from src.models.user_to_conversation import user_conversation
from src.models.friendship import friendships

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)

    conversations = relationship("Conversation", secondary=user_conversation, back_populates="users")
    friends = relationship(
        "User",
        secondary=friendships,
        primaryjoin=id == friendships.c.user_id,
        secondaryjoin=id == friendships.c.friend_id
    )