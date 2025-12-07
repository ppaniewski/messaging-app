from sqlalchemy import Table, Column, ForeignKey

from src.models.base import Base

friend_requests = Table(
    "friend_requests",
    Base.metadata,
    Column("sender_id", ForeignKey("users.id"), primary_key=True),
    Column("receiver_id", ForeignKey("users.id"), primary_key=True)
)