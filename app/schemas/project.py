from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    team_id: int

class ProjectUpdate(ProjectBase):
    pass

class ProjectInDBBase(ProjectBase):
    id: int
    team_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Project(ProjectInDBBase):
    pass

class ProjectInDB(ProjectInDBBase):
    pass