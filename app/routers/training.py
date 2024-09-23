from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User as UserModel
from app.schemas.training import TrainingDataCreate, TrainingResponse
from app.services import training_service, project_service, team_service

router = APIRouter()

@router.post('/upload', response_model=TrainingResponse)
async def upload_training_data(
    request: Request,
    project_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
):
    # Get the project
    project = project_service.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    # Check if the user is a member of the team that owns the project
    if not team_service.is_team_member(db, project.team, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to upload training data for this project"
        )
    
    # Proceed with upload
    data = TrainingDataCreate(
        project_id=project_id,
        file_name=file.filename,
        content_type=file.content_type
    )
    file_content = await file.read()
    
    try:
        training_data = await training_service.store_training_data(
            db, data, file_content, current_user, request.client.host
        )
        training_service.trigger_training_job(project_id, current_user, request.client.host, db)
        return TrainingResponse(status='Data uploaded, training job started', file_url=training_data.file_url)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get('/status/{project_id}', response_model=TrainingResponse)
async def get_model_status(
    request: Request,
    project_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
):
    # Get the project
    project = project_service.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    # Check if the user is a member of the team that owns the project
    if not team_service.is_team_member(db, project.team, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this project's training data"
        )
    
    try:
        status, file_url = await training_service.get_model_status(db, project_id, current_user, request.client.host)
        return TrainingResponse(status=status, file_url=file_url)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))