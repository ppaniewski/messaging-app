from datetime import datetime, timedelta, timezone

from fastapi import Depends
from sqlalchemy.orm import Session as DbSession

from src.config.database import get_db
from src.models.session import Session

class SessionRepository:
    def __init__(self, db: DbSession = Depends(get_db)):
        self.db = db

    def get(self, token_hash: str) -> Session | None:
        self.db.query(Session).where(Session.refresh_token_hash == token_hash).scalar()

    def update(self, session_id: int, last_used_at: datetime | None = None, revoked_at: datetime | None = None):
        session = self.db.get(Session, session_id)
        if (session == None):
            raise Exception("No session found by this id")

        if last_used_at:
            session.last_used_at = last_used_at
        if revoked_at:
            session.revoked_at = revoked_at

        self.db.commit()

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
        self.db.commit()