from datetime import datetime, timedelta, timezone

from fastapi import Depends
from sqlalchemy.orm import Session as DbSession

from src.config.database import get_db
from src.models.session import Session

class SessionRepository:
    def __init__(self, db: DbSession):
        self.db = db

    def commit(self):
        self.db.commit()

    def get(self, token_hash: str) -> Session | None:
        return self.db.query(Session).where(Session.refresh_token_hash == token_hash).first()

    def create(
        self, token_hash: str, user_id: int, user_agent: str | None, 
        expiration_date: datetime, rotated_from_id: int | None = None
    ):
        current_date = datetime.now(timezone.utc)

        new_session = Session(
            user_id=user_id,
            refresh_token_hash=token_hash,
            user_agent=user_agent,
            created_at=current_date,
            expires_at=expiration_date,
            rotated_from_id=rotated_from_id
        )

        self.db.add(new_session)