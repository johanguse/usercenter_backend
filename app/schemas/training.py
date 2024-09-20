from typing import List

from pydantic import BaseModel


class TrainingData(BaseModel):
    user_id: int
    bot_id: int
    data: List[dict]


class TrainingResponse(BaseModel):
    status: str
