from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.repositories.subject_repository import SubjectRepository
from app.schemas.subject import SubjectCreate, SubjectUpdate, SubjectResponse
from fastapi import HTTPException, status

class SubjectService:
    def __init__(self, db: AsyncSession):
        self.subject_repository = SubjectRepository(db)

    async def get_all_subjects(self) -> List[SubjectResponse]:
        subjects = await self.subject_repository.get_all_subjects()
        return [SubjectResponse.model_validate(subject) for subject in subjects]
    
    async def get_subject_by_id(self, subject_id: int) -> SubjectResponse:
        subject = await self.subject_repository.get_by_id(subject_id)
        if not subject:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")
        return SubjectResponse.model_validate(subject)

    async def create_subject(self, subject_data: SubjectCreate) -> SubjectResponse:
        existing_subject = await self.subject_repository.get_by_name(subject_data.name)
        if existing_subject:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Subject with this name already exists")
        subject = await self.subject_repository.create_subject(subject_data)
        return SubjectResponse.model_validate(subject)

    async def update_subject(self, subject_id: int, subject_data: SubjectUpdate) -> SubjectResponse:
        subject = await self.subject_repository.get_by_id(subject_id)
        if not subject:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")
        updated_subject = await self.subject_repository.update_subject(subject_id, subject_data)
        return SubjectResponse.model_validate(updated_subject)

    async def delete_subject(self, subject_id: int) -> None:
        subject = await self.subject_repository.get_by_id(subject_id)
        if not subject:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")
        await self.subject_repository.delete_subject(subject_id)
    