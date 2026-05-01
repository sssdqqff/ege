from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from fastapi import HTTPException, status

class TaskService:
    def __init__(self, db: AsyncSession):
        self.task_repository = TaskRepository(db)
    
    async def get_all_tasks(self) -> List[TaskResponse]:
        tasks = await self.task_repository.get_all_tasks()
        return [TaskResponse.model_validate(task) for task in tasks]
    
    async def get_task_by_id(self, task_id: int) -> TaskResponse:
        task = await self.task_repository.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return TaskResponse.model_validate(task)
    
    async def create_task(self, task_data: TaskCreate) -> TaskResponse:
        existing_task = await self.task_repository.get_by_name(task_data.name)
        if existing_task:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task with this name already exists")
        task = await self.task_repository.create_task(task_data)
        return TaskResponse.model_validate(task)
    
    async def update_task(self, task_id: int, task_data: TaskUpdate) -> TaskResponse:
        task = await self.task_repository.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        updated_task = await self.task_repository.update_task(task_id, task_data)
        return TaskResponse.model_validate(updated_task)
    
    async def delete_task(self, task_id: int) -> None:
        task = await self.task_repository.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        await self.task_repository.delete_task(task_id)
