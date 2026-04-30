from pydantic import BaseModel, Field

class AttemptBase(BaseModel):
    is_correct: bool = Field(..., description="Indicates if the user's answer is correct")

class AttemptCreate(BaseModel):
    pass

class AttemptUpdate(BaseModel):
    pass

class AttemptResponse(AttemptBase):
    pass