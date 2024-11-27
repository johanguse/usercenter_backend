from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User as UserModel
from app.schemas.training import TrainingDataCreate, TrainingResponse
from app.services import training_service

router = APIRouter()


@router.post('/upload', response_model=TrainingResponse)
async def upload_training_data(
    data: TrainingDataCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
):
    if current_user.id != data.user_id:
        raise HTTPException(
            status_code=403,
            detail='Not authorized to upload training data for this user',
        )
    await training_service.store_training_data(db, data)
    training_service.trigger_training_job(data.user_id, data.bot_id)
    return TrainingResponse(status='Data uploaded, training job started')


@router.get('/status/{bot_id}', response_model=TrainingResponse)
async def get_model_status(
    bot_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
):
    status = await training_service.get_model_status(
        db, current_user.id, bot_id
    )
    return TrainingResponse(status=status)
