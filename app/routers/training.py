from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.security import get_current_active_user
from app.models.user import User as UserModel
from app.schemas.training import TrainingDataCreate, TrainingResponse
from app.services import training_service

router = APIRouter()


@router.post("/", response_model=TrainingResponse)
async def create_training_data(
    training_data: TrainingDataCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(get_current_active_user)
):
    return await training_service.create_training_data(db, training_data, current_user)


@router.post("/upload", response_model=TrainingResponse)
async def upload_training_data(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(get_current_active_user)
):
    return await training_service.upload_training_data(db, file, current_user)


@router.get("/", response_model=list[TrainingResponse])
async def get_training_data(
    db: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(get_current_active_user)
):
    return await training_service.get_training_data(db, current_user)


@router.get("/{training_id}", response_model=TrainingResponse)
async def get_training_data_by_id(
    training_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(get_current_active_user)
):
    training_data = await training_service.get_training_data_by_id(db, training_id, current_user)
    if training_data is None:
        raise HTTPException(status_code=404, detail="Training data not found")
    return training_data


@router.delete("/{training_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_training_data(
    training_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(get_current_active_user)
):
    deleted = await training_service.delete_training_data(db, training_id, current_user)
    if not deleted:
        raise HTTPException(status_code=404, detail="Training data not found")
