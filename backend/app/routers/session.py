from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..database import get_db
from app.services.session_service import SessionService
from app.schemas.session import SessionResponse, SessionCreate, SessionUpdate