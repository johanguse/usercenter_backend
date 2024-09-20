from pydantic import BaseModel


class ChatMessage(BaseModel):
    user_id: int
    bot_id: int
    message: str


class ChatResponse(BaseModel):
    response: str
