from typing import Annotated
from fastapi import APIRouter, Request, Depends

from src.services.user_service import UserService
from src.utils.security import verify_access_token

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(verify_access_token)]
)

@router.get("/friends", status_code=200)
async def get_friends(request: Request, user_service: UserService = Depends()):
    return user_service.get_friends(request.state.user_id)