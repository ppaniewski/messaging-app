from fastapi import Depends, Response
from argon2 import PasswordHasher, exceptions
from sqlalchemy.orm import Session

from src.repositories.user_repository import UserRepository
from src.repositories.session_repository import SessionRepository
from src.schemas.user_schemas import UserIn, UserOut, UserOutLogin
from src.utils.security import create_access_token, issue_new_refresh_token, rotate_refresh_tokens, terminate_refresh_token, REFRESH_TOKEN_EXPIRATION_DAYS
from src.exceptions.exceptions import BadRequestException, UnauthorizedException, NotFoundException, ServerErrorException

class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
        self.session_repo = SessionRepository(db)

    def register(self, user: UserIn) -> UserOut:
        existing_user = self.user_repo.get_by_username(user.username)
        if existing_user:
            raise BadRequestException("Username already taken")

        ph = PasswordHasher()
        user.password = ph.hash(user.password)
        new_user = self.user_repo.create(user)
        
        self.user_repo.commit()

        return UserOut(id=new_user.id, username=new_user.username)
    
    def login(self, user: UserIn, response: Response, user_agent: str | None) -> UserOutLogin:
        existing_user = self.user_repo.get_by_username(user.username)
        if not existing_user:
            raise NotFoundException("User not found")
        
        ph = PasswordHasher()
        try:
            ph.verify(existing_user.password, user.password)
        except exceptions.VerifyMismatchError:
            raise UnauthorizedException("Incorrect password")
        
        try:
            access_token = create_access_token(existing_user.id)
        except Exception:
            raise ServerErrorException("Failed to issue access token")
    
        refresh_token = issue_new_refresh_token(existing_user.id, user_agent, self.session_repo)
        response.set_cookie(
            key="refresh-token", 
            value=refresh_token, 
            max_age=REFRESH_TOKEN_EXPIRATION_DAYS * 24 * 60 * 60,
            httponly=True, secure=False, samesite="strict"
        )
        
        return UserOutLogin(access_token=access_token, id=existing_user.id, username=existing_user.username)
    
    def logout(self, refresh_token: str, response: Response) -> None:
        response.delete_cookie(
            key="refresh-token",
            httponly=True, secure=False, samesite="strict"
        )

        terminate_refresh_token(refresh_token, self.session_repo)
    
    def refresh_access(self, refresh_token: str, response: Response) -> UserOutLogin:
        response.delete_cookie(
            key="refresh-token", 
            httponly=True, secure=False, samesite="strict"
        )

        data = rotate_refresh_tokens(refresh_token, self.session_repo)
        new_refresh_token = data["new_token"]
        expiration_date = data["expiration_date"]
        user_id = data["user_id"]

        username = ""
        user = self.user_repo.get_by_id(user_id)
        if user != None:
            username = user.username

        response.set_cookie(
            key="refresh-token",
            value=new_refresh_token,
            expires=expiration_date,
            httponly=True, secure=False, samesite="strict"
        )

        try:
            access_token = create_access_token(user_id)
        except Exception:
            raise ServerErrorException("Failed to issue access token")
        
        return UserOutLogin(access_token=access_token, id=user_id, username=username)