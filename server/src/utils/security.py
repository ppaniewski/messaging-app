import os
from datetime import datetime, timezone, timedelta
import secrets
import hashlib
from typing import Annotated

import jwt
from fastapi import Header, HTTPException, Request

from src.repositories.session_repository import SessionRepository

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

def verify_access_token(access_token: Annotated[str, Header()], request: Request):
    secret = os.getenv("JWT_SECRET")
    if not isinstance(secret, str):
        raise KeyError()

    try: 
        decoded = jwt.decode(
            access_token, secret, algorithms=["HS256"], 
            options={"require": ["exp", "iat"], "verify_exp": "verify_signature"}
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    request.state.user_id = decoded["user_id"]

def issue_new_refresh_token(user_id: int, user_agent: str | None) -> str:
    session_repository = SessionRepository()

    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    expiration_date = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRATION_DAYS)

    session_repository.create(token_hash, user_id, user_agent, expiration_date)

    return token

def rotate_refresh_tokens(refresh_token: str):
    session_repository = SessionRepository()

    token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
    previous_session = session_repository.get(token_hash)

    if not previous_session:
        raise Exception("No token matching")
    if previous_session.revoked_at != None:
        raise Exception("Refresh token already revoked")
    if previous_session.expires_at < datetime.now(timezone.utc):
        raise Exception("Expired refresh token")
    
    # Expire current session 
    current_time = datetime.now(timezone.utc)
    session_repository.update(previous_session.id, current_time, current_time)
    
    new_token = secrets.token_urlsafe(32)
    new_token_hash = hashlib.sha256(new_token.encode()).hexdigest()
    
    session_repository.create(
        new_token_hash, previous_session.user_id, previous_session.user_agent, 
        previous_session.expires_at, previous_session.id
    )

    return {
        "new_token": new_token,
        "expiration_date": previous_session.expires_at,
        "user_id": previous_session.user_id
    }