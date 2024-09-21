import time

from celery import Celery
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.training import ModelStatus, TrainingData
from app.schemas.training import TrainingDataCreate

celery_app = Celery('tasks', broker=settings.CELERY_BROKER_URL)

async def store_training_data(db: Session, data: TrainingDataCreate):
    db_data = TrainingData(
        user_id=data.user_id,
        bot_id=data.bot_id,
        data=data.data,
        status=ModelStatus.TRAINING
    )
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

def trigger_training_job(user_id: int, bot_id: int):
    train_model.delay(user_id, bot_id)

@celery_app.task
def train_model(user_id: int, bot_id: int):
    # This function would trigger your model training pipeline
    # For now, it's a placeholder
    time.sleep(10)  # Simulating training time
    
    db = SessionLocal()
    try:
        training_data = (
            db.query(TrainingData)
            .filter(TrainingData.user_id == user_id, TrainingData.bot_id == bot_id)
            .order_by(TrainingData.created_at.desc())
            .first()
        )
        if training_data:
            training_data.status = ModelStatus.COMPLETED
            db.commit()
    finally:
        db.close()

async def get_model_status(db: Session, user_id: int, bot_id: int):
    training_data = (
        db.query(TrainingData)
        .filter(TrainingData.user_id == user_id, TrainingData.bot_id == bot_id)
        .order_by(TrainingData.created_at.desc())
        .first()
    )
    if not training_data:
        raise HTTPException(status_code=404, detail='Model not found')
    return training_data.status.value
