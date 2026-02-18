from datetime import datetime
from typing import List

from pydantic import Field

from .user_schemas import UserOutConversation
from .base_schemas import CamelModel

class MessageBase(CamelModel):
    text: str = Field(min_length=1, max_length=10000)

class MessageIn(MessageBase):
    pass

class MessageOut(MessageBase):
    id: int
    user_id: int
    is_deleted: bool = False
    created_at: datetime

class MessageOutExtended(MessageOut):
    conversation_id: int

class ConversationOut(CamelModel):
    id: int
    is_group_chat: bool
    name: str | None = None
    messages: List[MessageOut]
    users: List[UserOutConversation]