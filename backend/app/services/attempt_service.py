from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.repositories.attempt_repository import AttemptRepository
from app.schemas.attempt import AttemptCreate, AttemptUpdate, AttemptResponse
from fastapi import HTTPException, status

class AttemptService:
    def __init__(self, db: AsyncSession):
        self.attempt_repository = AttemptRepository(db)

    async def get_all_attempts(self) -> List[AttemptResponse]:
        attempts = await self.attempt_repository.get_all_attempts()
        return [AttemptResponse.model_validate(attempt) for attempt in attempts]
    
    async def get_attempt_by_id(self, attempt_id: int) -> AttemptResponse:
        attempt = await self.attempt_repository.get_by_id(attempt_id)
        if not attempt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found")
        return AttemptResponse.model_validate(attempt)
    
    async def create_attempt(self, attempt_data: AttemptCreate) -> AttemptResponse:
        existing_attempt = await self.attempt_repository.get_by_name(attempt_data.name)
        if existing_attempt:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Attempt with this name already exists")
        attempt = await self.attempt_repository.create_attempt(attempt_data)
        return AttemptResponse.model_validate(attempt)
    
    async def update_attempt(self, attempt_id: int, attempt_data: AttemptUpdate) -> AttemptResponse:
        attempt = await self.attempt_repository.get_by_id(attempt_id)
        if not attempt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found")
        updated_attempt = await self.attempt_repository.update_attempt(attempt_id, attempt_data)
        return AttemptResponse.model_validate(updated_attempt)
    
    async def delete_attempt(self, attempt_id: int) -> None:
        attempt = await self.attempt_repository.get_by_id(attempt_id)
        if not attempt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found")
        await self.attempt_repository.delete_attempt(attempt_id)