from fastapi import Depends, HTTPException, Response
from argon2 import PasswordHasher, exceptions

from src.repositories.user_repository import UserRepository
from src.schemas.user_schemas import UserIn, UserOut, UserOutLogin
from src.utils.security import create_access_token, issue_new_refresh_token, rotate_refresh_tokens, REFRESH_TOKEN_EXPIRATION_DAYS

class AuthService:
    def __init__(self, user_repository: UserRepository = Depends()):
        self.user_repository = user_repository

    def register(self, user: UserIn) -> UserOut:
        existing_user = self.user_repository.get_by_username(user.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already taken")

        ph = PasswordHasher()
        user.password = ph.hash(user.password)
        new_user = self.user_repository.create(user)
        return UserOut.model_validate(new_user)
    
    def login(self, user: UserIn, response: Response, user_agent: str | None) -> UserOutLogin:
        existing_user = self.user_repository.get_by_username(user.username)
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        ph = PasswordHasher()
        try:
            ph.verify(existing_user.password, user.password)
        except exceptions.VerifyMismatchError:
            raise HTTPException(status_code=401, detail="Incorrect password")
        
        try:
            access_token = create_access_token(existing_user.id)
        except Exception:
            raise HTTPException(status_code=500, detail="Failed to issue access token")
    
        refresh_token = issue_new_refresh_token(existing_user.id, user_agent)
        response.set_cookie(
            key="refresh-token", 
            value=refresh_token, 
            max_age=REFRESH_TOKEN_EXPIRATION_DAYS * 24 * 60 * 60,
            httponly=True, secure=False, samesite="strict"
        )
        
        return UserOutLogin(id=existing_user.id, username=existing_user.username, access_token=access_token)
    
    def refresh_access(self, refresh_token: str, response: Response) -> str:
        response.delete_cookie(
            key="refresh-token", 
            httponly=True, secure=False, samesite="strict"
        )

        data = rotate_refresh_tokens(refresh_token)
        new_refresh_token = data["new_token"]
        expiration_date = data["expiration_date"]
        user_id = data["user_id"]

        response.set_cookie(
            key="refresh-token",
            value=new_refresh_token,
            expires=expiration_date,
            httponly=True, secure=False, samesite="strict"
        )

        try:
            access_token = create_access_token(user_id)
        except Exception:
            raise HTTPException(status_code=500, detail="Failed to issue access token")
        
        return access_token