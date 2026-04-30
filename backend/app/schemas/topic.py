from pydantic import BaseModel, ConfigDict, EmailStr, Field

class SubjectBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Subject name")
    description: str = Field(..., min_length=10, max_length=500, description="Subject description")
    is_active: bool = Field(default=True, description="Indicates if the subject is active")

class SubjectCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Subject name")
    description: str = Field(..., min_length=10, max_length=500, description="Subject description")

class SubjectUpdate(BaseModel):
    name: str | None = Field(None, min_length=3, max_length=50)
    description: str | None = Field(None, min_length=10, max_length=500)

class SubjectResponse(SubjectBase):
    id: int = Field(..., description="Subject unique identifier")

    model_config = ConfigDict(from_attributes=True)