from pydantic import BaseModel, ConfigDict, EmailStr, Field

class TopicBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Topic name")
    description: str = Field(..., min_length=10, max_length=500, description="Topic description")
    is_active: bool = Field(default=True, description="Indicates if the topic is active")

class TopicCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Topic name")
    description: str = Field(..., min_length=10, max_length=500, description="Topic description")

class TopicUpdate(BaseModel):
    name: str | None = Field(None, min_length=3, max_length=50)
    description: str | None = Field(None, min_length=10, max_length=500)

class TopicResponse(TopicBase):
    id: int = Field(..., description="Topic unique identifier")

    model_config = ConfigDict(from_attributes=True)