from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    nickname: str = Field(..., min_length=3, max_length=20, description="User's nickname")
    email: EmailStr = Field(..., description="User's email address")    
    is_active: bool = Field(default=True, description="Indicates if the user is active")

class UserCreate(BaseModel):
    nickname: str = Field(..., min_length=3, max_length=20, description="User's nickname")
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=6, max_length=100, description="User's password")

class UserUpdate(BaseModel):
    nickname: str | None = Field(None, min_length=3, max_length=20)
    email: EmailStr | None = Field(None, description="User's email address")

class UserResponse(UserBase):
    id: int = Field(..., description="User's unique identifier")
    xp: int = Field(..., description="User's experience points")
    level: int = Field(..., description="User's level")
    last_login: Optional[datetime] = Field(..., description="Timestamp of user's last login")
    streak: int = Field(..., description="User's current streak")
    role: str = Field(..., description="User's role")
    avatar_url: Optional[str] = Field(..., description="URL of user's avatar")

    model_config = ConfigDict(from_attributes=True)