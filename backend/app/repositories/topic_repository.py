from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from ..models import Topic
from ..schemas import TopicCreate, TopicUpdate

class TopicRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_topics(self) -> List[Topic]:
        stmt = select(Topic)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def get_by_id(self, topic_id: int) -> Optional[Topic]:
        stmt = select(Topic).where(Topic.id == topic_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_name(self, name: str) -> Optional[Topic]:
        stmt = select(Topic).where(Topic.name == name)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def update_topic(self, topic_id: int, topic_data: TopicUpdate) -> Optional[Topic]:
        topic = await self.get_by_id(topic_id)
        if not topic:
            return None

        for key, value in topic_data.model_dump(exclude_unset=True).items():
            setattr(topic, key, value)

        try:
            await self.db.commit()
            await self.db.refresh(topic)
        except SQLAlchemyError:
            await self.db.rollback()
            raise

        return topic

    async def create_topic(self, topic_data: TopicCreate) -> Topic:
        new_topic = Topic(**topic_data.model_dump())

        try:
            self.db.add(new_topic)
            await self.db.commit()
            await self.db.refresh(new_topic)
        except SQLAlchemyError:
            await self.db.rollback()
            raise

        return new_topic
    
    async def delete_topic(self, topic_id: int) -> bool:
        topic = await self.get_by_id(topic_id)
        if not topic:
            return False

        try:
            self.db.delete(topic)
            await self.db.commit()
            return True
        except SQLAlchemyError:
            await self.db.rollback()
            raise