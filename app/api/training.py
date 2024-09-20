from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_token
from app.schemas.training import TrainingData, TrainingResponse
from app.services import training_service

router = APIRouter()


@router.post('/upload', response_model=TrainingResponse)
async def upload_training_data(
    data: TrainingData,
    db: Session = Depends(get_db),
    current_user=Depends(verify_token),
):
    if current_user.id != data.user_id:
        raise HTTPException(
            status_code=403,
            detail='Not authorized to upload training data for this user',
        )
    await training_service.store_training_data(db, data)
    training_service.trigger_training_job(data.user_id, data.bot_id)
    return TrainingResponse(status='Data uploaded, training job started')


@router.get('/status/{user_id}/{bot_id}', response_model=TrainingResponse)
async def get_model_status(
    user_id: int,
    bot_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(verify_token),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail='Not authorized to access this model status',
        )
    status = await training_service.get_model_status(db, user_id, bot_id)
    return TrainingResponse(status=status)
