from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.repositories.session_repository import SessionRepository
from app.schemas.session import SessionCreate, SessionUpdate, SessionResponse
from fastapi import HTTPException, status

class SessionService:
    def __init__(self, db: AsyncSession):
        self.session_repository = SessionRepository(db)

    async def get_sessions_by_user(self, user_id: int) -> List[SessionResponse]:
        sessions = await self.session_repository.get_sessions_by_user(user_id)
        return [SessionResponse.model_validate(session) for session in sessions]

    async def get_session_by_id(self, session_id: int) -> SessionResponse:
        session = await self.session_repository.get_session_by_id(session_id)
        if not session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
        return SessionResponse.model_validate(session)

    async def create_session(self, session_data: SessionCreate, user_id: int) -> SessionResponse:
        session = await self.session_repository.create_session(session_data, user_id)
        return SessionResponse.model_validate(session)

    async def update_session(self, session_id: int, session_data: SessionUpdate) -> SessionResponse:
        session = await self.session_repository.update_session(session_id, session_data)
        if not session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
        return SessionResponse.model_validate(session)