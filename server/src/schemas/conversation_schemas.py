from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from .user_schemas import UserOut

class MessageBase(BaseModel):
    text: str = Field(min_length=1, max_length=10000)

class MessageIn(MessageBase):
    pass

class MessageOut(MessageBase):
    id: int
    user_id: int
    is_deleted: bool = False
    created_at: datetime

class ConversationOut(BaseModel):
    id: int
    is_group_chat: bool
    name: str | None = None
    messages: List[MessageOut]
    users: List[UserOut]