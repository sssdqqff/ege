from pydantic import BaseModel, ConfigDict, EmailStr, Field

class TaskBase(BaseModel):
    condition: str = Field(..., min_length=10, description="Task condition")
    difficulty: str = Field(default="medium", description="Difficulty level of the task (easy, medium, hard)")
    is_active: bool = Field(default=True, description="Indicates if the task is active")

class TaskCreate(BaseModel):
    condition: str = Field(..., min_length=10, description="Task condition")
    difficulty: str = Field(default="medium", description="Difficulty level of the task (easy, medium, hard)")

class TaskUpdate(BaseModel):
    condition: str | None = Field(None, min_length=10)
    difficulty: str | None = Field(None)

class TaskResponse(TaskBase):
    id: int = Field(..., description="Task unique identifier")

    model_config = ConfigDict(from_attributes=True)