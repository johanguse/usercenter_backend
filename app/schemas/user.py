from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    name: Optional[str] = None
    role: str


class UserCreate(schemas.BaseUserCreate):
    name: Optional[str] = None
    role: str = 'member'


class UserUpdate(schemas.BaseUserUpdate):
    name: Optional[str] = None
    role: Optional[str] = None
