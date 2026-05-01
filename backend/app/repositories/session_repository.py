from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional

from app.models.session import Session
from app.schemas.session import SessionCreate, SessionUpdate


class SessionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_session(self, session_data: SessionCreate, user_id: int) -> Session:
        new_session = Session(**session_data.model_dump(), user_id=user_id)
        self.db.add(new_session)
        try:
            await self.db.commit()
            await self.db.refresh(new_session)
            return new_session
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def get_sessions_by_user(self, user_id: int) -> List[Session]:
        result = await self.db.execute(select(Session).where(Session.user_id == user_id).order_by(Session.created_at.desc()))
        return result.scalars().all()

    async def get_session_by_id(self, session_id: int) -> Optional[Session]:
        result = await self.db.execute(select(Session).where(Session.id == session_id))
        return result.scalar_one_or_none()

    async def update_session(self, session_id: int, session_data: SessionUpdate) -> Optional[Session]:
        session = await self.get_session_by_id(session_id)
        if not session:
            return None
        for key, value in session_data.model_dump(exclude_unset=True).items():
            setattr(session, key, value)
        try:
            await self.db.commit()
            await self.db.refresh(session)
            return session
        except SQLAlchemyError:
            await self.db.rollback()
            raise