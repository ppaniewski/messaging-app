from typing import Annotated
from fastapi import APIRouter, Depends, Response, Header, Cookie

from src.config.database import get_db
from src.services.auth_service import AuthService
from src.schemas.user_schemas import UserIn, UserOut, UserOutLogin
from src.utils.security import verify_access_dependency

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)

@router.post("/register", status_code=201)
async def register_user(user: UserIn, db = Depends(get_db)) -> UserOut:
    service = AuthService(db)
    return service.register(user)

@router.post("/login", status_code=200)
async def login_user(
    response: Response,
    user: UserIn, 
    user_agent: Annotated[str | None, Header()] = None, 
    db = Depends(get_db)
) -> UserOutLogin:
    service = AuthService(db)
    return service.login(user, response, user_agent)

@router.post("/logout", status_code=204)
async def logout_user(
    response: Response, 
    refresh_token: Annotated[str, Cookie(alias="refresh-token")],
    db = Depends(get_db)
) -> None:
    service = AuthService(db)
    service.logout(refresh_token, response)

@router.post("/refresh", status_code=200)
async def refresh_access(
    response: Response, 
    refresh_token: Annotated[str, Cookie(alias="refresh-token")], 
    db = Depends(get_db)
) -> UserOutLogin:
    service = AuthService(db)
    return service.refresh_access(refresh_token, response)

@router.post("/verify", status_code=204, dependencies=[Depends(verify_access_dependency)])
async def verify_access() -> None:
    return None