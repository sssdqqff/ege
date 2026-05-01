from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from app.models.subject import Subject
from app.schemas.subject import SubjectCreate, SubjectUpdate

class SubjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_subjects(self) -> List[Subject]:
        stmt = select(Subject)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def get_subject_with_topics(self, subject_id: int) -> Optional[Subject]:
        stmt = select(Subject).options(selectinload(Subject.topics)).where(Subject.id == subject_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_id(self, subject_id: int) -> Optional[Subject]:
        stmt = select(Subject).where(Subject.id == subject_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Optional[Subject]:
        stmt = select(Subject).where(Subject.name == name)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def update_subject(self, subject_id: int, subject_data: SubjectUpdate) -> Optional[Subject]:
        subject = await self.get_by_id(subject_id)
        if not subject:
            return None
        for key, value in subject_data.model_dump(exclude_unset=True).items():
            setattr(subject, key, value)
        try:
            await self.db.commit()
            await self.db.refresh(subject)
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def create_subject(self, subject_data: SubjectCreate) -> Subject:
        new_subject = Subject(**subject_data.model_dump())
        try:
            self.db.add(new_subject)
            await self.db.commit()
            await self.db.refresh(new_subject)
        except SQLAlchemyError:
            await self.db.rollback()
            raise

        return new_subject
    
    async def delete_subject(self, subject_id: int) -> bool:
        subject = await self.get_by_id(subject_id)
        if not subject:
            return False

        try:
            self.db.delete(subject)
            await self.db.commit()
            return True
        except SQLAlchemyError:
            await self.db.rollback()
            raise