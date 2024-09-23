from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User as UserModel
from app.schemas.project import ProjectCreate, ProjectUpdate, Project, ProjectInDB
from app.services import project_service, team_service

router = APIRouter()

@router.post("/", response_model=Project)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    team = team_service.get_team(db, project.team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    if not team_service.is_team_member(db, team, current_user):
        raise HTTPException(status_code=403, detail="You don't have permission to create a project for this team")
    return project_service.create_project(db, project, current_user)

@router.get("/{project_id}", response_model=Project)
def read_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    project = project_service.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if not team_service.is_team_member(db, project.team, current_user):
        raise HTTPException(status_code=403, detail="You don't have permission to view this project")
    return project

@router.put("/{project_id}", response_model=Project)
def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    project = project_service.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if not team_service.is_team_member(db, project.team, current_user):
        raise HTTPException(status_code=403, detail="You don't have permission to update this project")
    return project_service.update_project(db, project, project_update)

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    project = project_service.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if not team_service.is_team_admin(db, project.team, current_user):
        raise HTTPException(status_code=403, detail="You don't have permission to delete this project")
    project_service.delete_project(db, project)
    return {"detail": "Project deleted successfully"}

@router.get("/team/{team_id}", response_model=List[Project])
def list_team_projects(
    team_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    team = team_service.get_team(db, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    if not team_service.is_team_member(db, team, current_user):
        raise HTTPException(status_code=403, detail="You don't have permission to view this team's projects")
    return project_service.get_team_projects(db, team_id)