from datetime import datetime

from pydantic import BaseModel, Field


class QuestionSchema(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime

    class Config:
        orm_mode = True


class QuestionCreate(BaseModel):
    subject: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)

