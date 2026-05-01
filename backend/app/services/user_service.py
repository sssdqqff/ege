from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from fastapi import HTTPException, status

class UserService:
    def __init__(self, db: AsyncSession):
        self.user_repository = UserRepository(db)

    async def get_all_users(self) -> List[UserResponse]:
        users = await self.user_repository.get_all_users()
        return [UserResponse.model_validate(user) for user in users]
    
    async def get_user_by_id(self, user_id: int) -> UserResponse:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserResponse.model_validate(user)
    
    async def create_user(self, user_data: UserCreate) -> UserResponse:
        existing_user = await self.user_repository.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")
        user = await self.user_repository.create_user(user_data)
        return UserResponse.model_validate(user)
    
    async def update_user(self, user_id: int, user_data: UserUpdate) -> UserResponse:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        updated_user = await self.user_repository.update_user(user_id, user_data)
        return UserResponse.model_validate(updated_user)
    
    async def delete_user(self, user_id: int) -> None:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        await self.user_repository.delete_user(user_id)