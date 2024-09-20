import time

from celery import Celery
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.training import ModelStatus, TrainingData

celery_app = Celery('tasks', broker=settings.CELERY_BROKER_URL)


async def store_training_data(db: Session, data):
    db_data = TrainingData(
        user_id=data.user_id, bot_id=data.bot_id, data=data.data
    )
    db.add(db_data)
    db.commit()


def trigger_training_job(user_id: int, bot_id: int):
    train_model.delay(user_id, bot_id)


@celery_app.task
def train_model(user_id: int, bot_id: int):
    # This function would trigger your model training pipeline
    # For now, it's a placeholder

    time.sleep(10)  # Simulating training time
    # Update model status in database
    db = SessionLocal()
    status = (
        db.query(ModelStatus)
        .filter(ModelStatus.user_id == user_id, ModelStatus.bot_id == bot_id)
        .first()
    )
    if status:
        status.status = 'Trained'
    else:
        status = ModelStatus(user_id=user_id, bot_id=bot_id, status='Trained')
        db.add(status)
    db.commit()
    db.close()


async def get_model_status(db: Session, user_id: int, bot_id: int):
    status = (
        db.query(ModelStatus)
        .filter(ModelStatus.user_id == user_id, ModelStatus.bot_id == bot_id)
        .first()
    )
    if not status:
        raise HTTPException(status_code=404, detail='Model not found')
    return status.status
