from typing import Annotated, List

from fastapi import APIRouter, Depends, Request, Path, Query

from src.utils.security import verify_access_token
from src.services.conversation_service import ConversationService
from src.schemas.conversation_schemas import MessageIn, MessageOut, ConversationOut

router = APIRouter(
    prefix="/conversations",
    tags=["conversations"],
    dependencies=[Depends(verify_access_token)]
)

@router.get("/", status_code=200)
async def get_conversations(
    request: Request, 
    message_limit: Annotated[int, Query(ge=1, lt=1000, description="Message limit per conversation")],
    conversation_service: ConversationService = Depends()
) -> List[ConversationOut]:
    return conversation_service.get_conversations(request.state.user_id, message_limit)

@router.get("/{conversation_id}", status_code=200)
async def get_conversation_messages(
    request: Request,
    conversation_id: Annotated[int, Path()],
    offset: Annotated[int, Query(ge=0, lt=1000000, description="Message offset")],
    amount: Annotated[int, Query(ge=1, lt=1000, description="Amount of messages")],
    conversation_service: ConversationService = Depends()
) -> List[MessageOut]:
    return conversation_service.get_conversation_messages(request.state.user_id, conversation_id, offset, amount)

@router.post("/messages/{recipient_username}", status_code=201)
async def send_user_message(
    request: Request, recipient_username: Annotated[str, Path()],
    message_in: MessageIn,
    conversation_service: ConversationService = Depends()
) -> MessageOut:
    return conversation_service.send_user_message(recipient_username, request.state.user_id, message_in.text)

@router.delete("/messages/{recipient_username}/{message_id}", status_code=200)
async def delete_user_message(
    request: Request,
    message_id: Annotated[int, Path()],
    conversation_service: ConversationService = Depends()
) -> MessageOut:
    return conversation_service.delete_user_message(request.state.user_id, message_id)