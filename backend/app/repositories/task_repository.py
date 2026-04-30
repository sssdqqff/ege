from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from ..models import Task
from ..schemas import TaskCreate, TaskUpdate

class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_tasks(self) -> List[Task]:
        stmt = select(Task).options(
            selectinload(Task.topic)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def get_by_id(self, task_id: int) -> Optional[Task]:
        stmt = select(Task).where(Task.id == task_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def update_task(self, task_id: int, task_data: TaskUpdate) -> Optional[Task]:
        task = await self.get_by_id(task_id)
        if not task:
            return None

        for key, value in task_data.model_dump(exclude_unset=True).items():
            setattr(task, key, value)

        try:
            await self.db.commit()
            await self.db.refresh(task)
        except SQLAlchemyError:
            await self.db.rollback()
            raise

        return task
    
    async def create_task(self, task_data: TaskCreate) -> Task:
        new_task = Task(**task_data.model_dump())

        try:
            self.db.add(new_task)
            await self.db.commit()
            await self.db.refresh(new_task)
        except SQLAlchemyError:
            await self.db.rollback()
            raise

        return new_task
    
    async def delete_task(self, task_id: int) -> bool:
        task = await self.get_by_id(task_id)
        if not task:
            return False

        try:
            self.db.delete(task)
            await self.db.commit()
            return True
        except SQLAlchemyError:
            await self.db.rollback()
            raise