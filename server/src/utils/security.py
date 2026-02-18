import os
from datetime import datetime, timezone, timedelta
import secrets
import hashlib
from typing import Annotated

import jwt
from fastapi import Header, Request

from src.repositories.session_repository import SessionRepository
from src.exceptions.exceptions import BadRequestException, NotFoundException, ServerErrorException, UnauthorizedException

REFRESH_TOKEN_EXPIRATION_DAYS = 30
ACCESS_TOKEN_EXPIRATION_MINS = 15

def create_access_token(user_id: int) -> str:
    current_time = datetime.now(timezone.utc)

    payload = {
        "user_id": user_id,
        "exp": current_time + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINS),
        "iat": current_time
    }

    secret = os.getenv("JWT_SECRET")
    if not isinstance(secret, str):
        raise KeyError()

    return jwt.encode(payload, secret, algorithm="HS256")

def verify_access_dependency(authorization: Annotated[str, Header()], request: Request):
    access_token = authorization.split(" ")[1]

    secret = os.getenv("JWT_SECRET")
    if not isinstance(secret, str):
        raise ServerErrorException("Could not load JWT secret")

    try: 
        decoded = jwt.decode(
            access_token, secret, algorithms=["HS256"], 
            options={"require": ["exp", "iat"], "verify_exp": "verify_signature"}
        )
    except Exception:
        raise UnauthorizedException("Invalid access token")
    
    request.state.user_id = decoded["user_id"]

def verify_access_token(access_token: str) -> int:
    secret = os.getenv("JWT_SECRET")
    if not isinstance(secret, str):
        raise ServerErrorException("Could not load JWT secret")
    
    try: 
        decoded = jwt.decode(
            access_token, secret, algorithms=["HS256"], 
            options={"require": ["exp", "iat"], "verify_exp": "verify_signature"}
        )
    except Exception:
        raise UnauthorizedException("Invalid access token")
    
    return decoded["user_id"]
    

def issue_new_refresh_token(user_id: int, user_agent: str | None, session_repo: SessionRepository) -> str:
    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    expiration_date = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRATION_DAYS)

    session_repo.create(token_hash, user_id, user_agent, expiration_date)
    session_repo.commit()

    return token

def terminate_refresh_token(refresh_token: str, session_repo: SessionRepository):
    token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
    current_session = session_repo.get(token_hash)

    if not current_session:
        raise NotFoundException("No refresh token matching")
    if current_session.revoked_at != None:
        raise BadRequestException("Refresh token already revoked")
    if current_session.expires_at < datetime.now(timezone.utc):
        raise BadRequestException("Expired refresh token")

    current_time = datetime.now(timezone.utc)
    current_session.last_used_at = current_time
    current_session.revoked_at = current_time

    session_repo.commit()

def rotate_refresh_tokens(refresh_token: str, session_repo: SessionRepository):
    token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
    previous_session = session_repo.get(token_hash)

    if not previous_session:
        raise NotFoundException("No refresh token matching")
    if previous_session.revoked_at != None:
        raise BadRequestException("Refresh token already revoked")
    if previous_session.expires_at < datetime.now(timezone.utc):
        raise BadRequestException("Expired refresh token")
    
    # Expire current session 
    current_time = datetime.now(timezone.utc)
    previous_session.last_used_at = current_time
    previous_session.revoked_at = current_time
    
    new_token = secrets.token_urlsafe(32)
    new_token_hash = hashlib.sha256(new_token.encode()).hexdigest()
    
    session_repo.create(
        new_token_hash, previous_session.user_id, previous_session.user_agent, 
        previous_session.expires_at, previous_session.id
    )

    session_repo.commit()

    return {
        "new_token": new_token,
        "expiration_date": previous_session.expires_at,
        "user_id": previous_session.user_id
    }