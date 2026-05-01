from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.repositories.topic_repository import TopicRepository
from app.schemas.topic import TopicCreate, TopicUpdate, TopicResponse
from fastapi import HTTPException, status

class TopicService:
    def __init__(self, db: AsyncSession):
        self.topic_repository = TopicRepository(db)

    async def get_all_topics(self) -> List[TopicResponse]:
        topics = await self.topic_repository.get_all_topics()
        return [TopicResponse.model_validate(topic) for topic in topics]
    
    async def get_topic_by_id(self, topic_id: int) -> TopicResponse:
        topic = await self.topic_repository.get_by_id(topic_id)
        if not topic:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
        return TopicResponse.model_validate(topic)
    
    async def create_topic(self, topic_data: TopicCreate) -> TopicResponse:
        existing_topic = await self.topic_repository.get_by_name(topic_data.name)
        if existing_topic:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Topic with this name already exists")
        topic = await self.topic_repository.create_topic(topic_data)
        return TopicResponse.model_validate(topic)
    
    async def update_topic(self, topic_id: int, topic_data: TopicUpdate) -> TopicResponse:
        topic = await self.topic_repository.get_by_id(topic_id)
        if not topic:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
        updated_topic = await self.topic_repository.update_topic(topic_id, topic_data)
        return TopicResponse.model_validate(updated_topic)
    
    async def delete_topic(self, topic_id: int) -> None:
        topic = await self.topic_repository.get_by_id(topic_id)
        if not topic:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
        await self.topic_repository.delete_topic(topic_id)
