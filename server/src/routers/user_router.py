from typing import Annotated, List
from fastapi import APIRouter, Request, Depends, Query, Path

from src.services.user_service import UserService
from src.utils.security import verify_access_token
from src.schemas.user_schemas import UserOut

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(verify_access_token)]
)

@router.get("/", status_code=200)
async def get_users(user_service: UserService = Depends()) -> List[UserOut]:
    return user_service.get_users()

@router.get("/friends", status_code=200)
async def get_friends(request: Request, user_service: UserService = Depends()) -> List[UserOut]:
    return user_service.get_friends(request.state.user_id)

@router.get("/friends/sent_requests", status_code=200)
async def get_sent_requests(request: Request, user_service: UserService = Depends()) -> List[UserOut]:
    return user_service.get_sent_friend_requests(request.state.user_id)

@router.get("/friends/received_requests", status_code=200)
async def get_received_requests(request: Request, user_service: UserService = Depends()) -> List[UserOut]:
    return user_service.get_received_friend_requests(request.state.user_id)

@router.post("/friends/add/{friend_username}", status_code=204)
async def send_friend_request(
    request: Request, friend_username: Annotated[str, Path()], 
    user_service: UserService = Depends()
) -> None:
    user_service.send_friend_request(friend_username, request.state.user_id)

@router.delete("/friends/remove/{friend_username}", status_code=204)
async def remove_friend(
    request: Request, friend_username: Annotated[str, Path()],
    user_service: UserService = Depends()
) -> None:
    user_service.remove_friend(friend_username, request.state.user_id)

@router.post("/friends/accept_request/{friend_username}", status_code=204)
async def accept_friend_request(
    request: Request, friend_username: Annotated[str, Path()], 
    user_service: UserService = Depends()
) -> None:
    user_service.accept_friend_request(friend_username, request.state.user_id)

@router.post("/friends/decline_request/{friend_username}", status_code=204)
async def decline_friend_request(
    request: Request, friend_username: Annotated[str, Path()],
    user_service: UserService = Depends()
) -> None:
    user_service.decline_friend_request(friend_username, request.state.user_id)