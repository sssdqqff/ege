from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from ..models import Attempt
from ..schemas import AttemptCreate, AttemptUpdate

class AttemptRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_attempts(self) -> List[Attempt]:
        stmt = select(Attempt).options(
            selectinload(Attempt.task),
            selectinload(Attempt.user)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def get_by_id(self, attempt_id: int) -> Optional[Attempt]:
        stmt = select(Attempt).where(Attempt.id == attempt_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_task_id(self, task_id: int) -> List[Attempt]:
        stmt = select(Attempt).where(Attempt.task_id == task_id).options(
            selectinload(Attempt.user)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def get_by_user_id(self, user_id: int) -> List[Attempt]:
        stmt = select(Attempt).where(Attempt.user_id == user_id).options(
            selectinload(Attempt.task)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def create_attempt(self, attempt_data: AttemptCreate) -> Attempt:
        new_attempt = Attempt(**attempt_data.model_dump())

        try:
            self.db.add(new_attempt)
            await self.db.commit()
            await self.db.refresh(new_attempt)
        except SQLAlchemyError:
            await self.db.rollback()
            raise

        return new_attempt