from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal
from datetime import datetime


SessionType = Literal["practice", "exam", "challenge"]
SessionStatus = Literal["in_progress", "completed", "abandoned"]


class SessionBase(BaseModel):
    type: SessionType = Field(default="practice", description="Session type")
    status: SessionStatus = Field(default="in_progress", description="Session status")


class SessionCreate(SessionBase):
    pass


class SessionUpdate(BaseModel):
    status: Optional[SessionStatus] = None
    finished_at: Optional[datetime] = None


class SessionResponse(SessionBase):
    id: int
    user_id: int
    created_at: datetime
    finished_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)