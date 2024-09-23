from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User as UserModel
from app.schemas.team import TeamCreate, TeamInvite, TeamMemberResponse, TeamResponse
from app.services import team_service

router = APIRouter()

@router.post("/", response_model=TeamResponse)
def create_team(
    team: TeamCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    return team_service.create_team(db, team, current_user)

@router.post("/{team_id}/invite", response_model=TeamMemberResponse)
def invite_team_member(
    request: Request,
    team_id: int,
    invite: TeamInvite,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    team = team_service.get_team(db, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    if not team_service.is_team_admin(db, team, current_user):
        raise HTTPException(status_code=403, detail="You don't have permission to invite members to this team")
    try:
        return team_service.invite_team_member(db, team, invite, current_user, request.client.host)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{team_id}/members", response_model=List[TeamMemberResponse])
def get_team_members(
    team_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    team = team_service.get_team(db, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    if not team_service.is_team_member(db, team, current_user):
        raise HTTPException(status_code=403, detail="You don't have permission to view this team's members")
    return team_service.get_team_members(db, team)
