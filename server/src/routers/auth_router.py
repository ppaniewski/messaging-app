from typing import Annotated
from fastapi import APIRouter, Depends, Response, Header, Cookie

from src.services.auth_service import AuthService
from src.schemas.user_schemas import UserIn, UserOut, UserOutLogin

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register", status_code=201)
async def register_user(user: UserIn, auth_service: AuthService = Depends()) -> UserOut:
    return auth_service.register(user)

@router.post("/login", status_code=200)
async def login_user(
    response: Response, 
    user: UserIn, 
    user_agent: Annotated[str | None, Header()] = None, 
    auth_service: AuthService = Depends()
) -> UserOutLogin:
    return auth_service.login(user, response, user_agent)

@router.post("/refresh", status_code=200)
async def refresh_access(response: Response, refresh_token: Annotated[str, Cookie()], auth_service: AuthService = Depends()) -> str:
    return auth_service.refresh_access(refresh_token, response)