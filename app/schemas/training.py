from typing import List, Dict
from pydantic import BaseModel
from app.models.training import ModelStatus

class TrainingDataCreate(BaseModel):
    user_id: int
    bot_id: int
    data: List[Dict]

class TrainingDataInDB(TrainingDataCreate):
    id: int
    status: ModelStatus
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class TrainingResponse(BaseModel):
    status: str
