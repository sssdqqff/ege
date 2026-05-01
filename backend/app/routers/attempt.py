from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..database import get_db
from ..services import AttemptService
from ..schemas import AttekmptResponse, AttemptCreate, AttemptUpdate

router = APIRouter(prefix="/attempts", tags=["attempts"])

def get_attempt_service(db: AsyncSession = Depends(get_db)):
    return AttemptService(db)

@router.get("", response_model=List[AttekmptResponse], status_code=status.HTTP_200_OK)
async def get_all_attempts(service: AttemptService = Depends(get_attempt_service)):
    return await service.get_all_attempts()

@router.get("/{attempt_id}", response_model=AttekmptResponse, status_code=status.HTTP_200_OK)
async def get_attempt_by_id(attempt_id: int, service: AttemptService = Depends(get_attempt_service)):
    return await service.get_attempt_by_id(attempt_id)

@router.post("", response_model=AttekmptResponse, status_code=status.HTTP_201_CREATED)
async def create_attempt(attempt_data: AttemptCreate, service: AttemptService = Depends(get_attempt_service)):
    return await service.create_attempt(attempt_data)

@router.put("/{attempt_id}", response_model=AttekmptResponse, status_code=status.HTTP_200_OK)
async def update_attempt(attempt_id: int, attempt_data: AttemptUpdate, service: AttemptService = Depends(get_attempt_service)):
    return await service.update_attempt(attempt_id, attempt_data)

@router.delete("/{attempt_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attempt(attempt_id: int, service: AttemptService = Depends(get_attempt_service)):
    await service.delete_attempt(attempt_id)
