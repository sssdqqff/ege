from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..database import get_db
from app.services.session_service import SessionService
from app.schemas.session import SessionCreate, SessionUpdate, SessionResponse

router = APIRouter(prefix="/sessions", tags=["sessions"])


def get_session_service(db: AsyncSession = Depends(get_db)):
    return SessionService(db)


@router.get("", response_model=List[SessionResponse], status_code=status.HTTP_200_OK)
async def get_sessions(service: SessionService = Depends(get_session_service)):
    return await service.get_sessions()


@router.get("/{session_id}", response_model=SessionResponse, status_code=status.HTTP_200_OK)
async def get_session_by_id(session_id: int, service: SessionService = Depends(get_session_service)):
    return await service.get_session_by_id(session_id)


@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(session_data: SessionCreate, service: SessionService = Depends(get_session_service)):
    return await service.create_session(session_data)


@router.put("/{session_id}", response_model=SessionResponse, status_code=status.HTTP_200_OK)
async def update_session(session_id: int, session_data: SessionUpdate, service: SessionService = Depends(get_session_service)):
    return await service.update_session(session_id, session_data)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(session_id: int, service: SessionService = Depends(get_session_service)):
    await service.delete_session(session_id)