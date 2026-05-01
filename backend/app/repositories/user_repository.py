from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_users(self) -> List[User]:
        stmt = select(User)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, user_id: int) -> Optional[User]:
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[User]:
        stmt = select(User).where(User.username == username)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(self, user_data: UserCreate) -> User:
        new_user = User(**user_data.model_dump())

        try:
            self.db.add(new_user)
            await self.db.commit()
            await self.db.refresh(new_user)
        except SQLAlchemyError:
            await self.db.rollback()
            raise

        return new_user

    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        user = await self.get_by_id(user_id)
        if not user:
            return None

        for key, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)

        try:
            await self.db.commit()
            await self.db.refresh(user)
        except SQLAlchemyError:
            await self.db.rollback()
            raise

        return user

    async def delete_user(self, user_id: int) -> bool:
        user = await self.get_by_id(user_id)
        if not user:
            return False

        try:
            self.db.delete(user)
            await self.db.commit()
            return True
        except SQLAlchemyError:
            await self.db.rollback()
            raise