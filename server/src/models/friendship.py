from sqlalchemy import Table, Column, ForeignKey

from src.models.base import Base

friendships = Table(
    "friendships",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("friend_id", ForeignKey("users.id"), primary_key=True)
)