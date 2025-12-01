import datetime

from sqlalchemy import String, func, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.models.conversation import Conversation

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    contents: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id"))

    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="messages")