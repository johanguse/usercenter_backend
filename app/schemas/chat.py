from datetime import datetime

from pydantic import BaseModel


class ChatMessageCreate(BaseModel):
    project_id: int
    user_id: int
    message: str


class ChatMessage(ChatMessageCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    response: str
