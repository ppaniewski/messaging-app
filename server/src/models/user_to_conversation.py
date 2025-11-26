from sqlalchemy import Table, Column, ForeignKey

from src.models.base import Base

user_conversation = Table(
    "user_conversation",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("conversation_id", ForeignKey("conversations.id"), primary_key=True)
)