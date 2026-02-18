from typing import Annotated, List

from fastapi import APIRouter, Depends, Request, Path, Query

from src.config.database import get_db
from src.utils.security import verify_access_dependency
from src.services.conversation_service import ConversationService
from src.schemas.conversation_schemas import MessageIn, MessageOut, MessageOutExtended, ConversationOut

router = APIRouter(
    prefix="/api/conversations",
    tags=["conversations"],
    dependencies=[Depends(verify_access_dependency)]
)

@router.get("", status_code=200)
async def get_conversations(
    request: Request, 
    message_limit: Annotated[int, Query(ge=1, lt=1000, description="Message limit per conversation")],
    limit: Annotated[int | None, Query()] = None,
    offset: Annotated[int | None, Query()] = None,
    db = Depends(get_db)
) -> List[ConversationOut]:
    service = ConversationService(db)
    return service.get_conversations(request.state.user_id, message_limit, limit, offset)

@router.get("/{conversation_id}", status_code=200)
async def get_conversation_messages(
    request: Request,
    conversation_id: Annotated[int, Path()],
    offset: Annotated[int, Query(ge=0, lt=1000000, description="Message offset")],
    amount: Annotated[int, Query(ge=1, lt=1000, description="Amount of messages")],
    db = Depends(get_db)
) -> List[MessageOut]:
    service = ConversationService(db)
    return service.get_conversation_messages(request.state.user_id, conversation_id, offset, amount)

@router.post("/messages/{recipient_id}", status_code=201)
async def send_user_message(
    request: Request, recipient_id: Annotated[int, Path()],
    message_in: MessageIn,
    db = Depends(get_db)
) -> MessageOutExtended:
    service = ConversationService(db)
    return service.send_user_message(recipient_id, request.state.user_id, message_in.text)

@router.delete("/messages/{message_id}", status_code=200)
async def delete_user_message(
    request: Request,
    message_id: Annotated[int, Path()],
    db = Depends(get_db)
) -> MessageOutExtended:
    service = ConversationService(db)
    return service.delete_user_message(request.state.user_id, message_id)