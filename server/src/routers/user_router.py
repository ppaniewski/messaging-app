from typing import Annotated, List
from fastapi import APIRouter, Request, Depends, Query, Path

from src.config.database import get_db
from src.services.user_service import UserService
from src.utils.security import verify_access_dependency
from src.schemas.user_schemas import UserOut

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    dependencies=[Depends(verify_access_dependency)]
)

@router.get("", status_code=200)
async def get_users(
    match_string: Annotated[str | None, Query(description="The initial string to match the username")] = None,
    limit: Annotated[int | None, Query()] = None,
    offset: Annotated[int | None, Query()] = None,
    db = Depends(get_db)
) -> List[UserOut]:
    service = UserService(db)
    return service.get_users(match_string, limit, offset)

@router.get("/friends", status_code=200)
async def get_friends(request: Request, db = Depends(get_db)) -> List[UserOut]:
    service = UserService(db)
    return service.get_friends(request.state.user_id)

@router.get("/friends/sent_requests", status_code=200)
async def get_sent_requests(request: Request, db = Depends(get_db)) -> List[UserOut]:
    service = UserService(db)
    return service.get_sent_friend_requests(request.state.user_id)

@router.get("/friends/received_requests", status_code=200)
async def get_received_requests(request: Request, db = Depends(get_db)) -> List[UserOut]:
    service = UserService(db)
    return service.get_received_friend_requests(request.state.user_id)

@router.post("/friends/add/{friend_id}", status_code=204)
async def send_friend_request(
    request: Request, friend_id: Annotated[int, Path()], 
    db = Depends(get_db)
) -> None:
    service = UserService(db)
    service.send_friend_request(friend_id, request.state.user_id)

@router.delete("/friends/remove/{friend_id}", status_code=204)
async def remove_friend(
    request: Request, friend_id: Annotated[int, Path()],
    db = Depends(get_db)
) -> None:
    service = UserService(db)
    service.remove_friend(friend_id, request.state.user_id)

@router.post("/friends/accept_request/{friend_id}", status_code=204)
async def accept_friend_request(
    request: Request, friend_id: Annotated[int, Path()], 
    db = Depends(get_db)
) -> None:
    service = UserService(db)
    service.accept_friend_request(friend_id, request.state.user_id)

@router.post("/friends/decline_request/{friend_id}", status_code=204)
async def decline_friend_request(
    request: Request, friend_id: Annotated[int, Path()],
    db = Depends(get_db)
) -> None:
    service = UserService(db)
    service.decline_friend_request(friend_id, request.state.user_id)