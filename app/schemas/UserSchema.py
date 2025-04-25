from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.User.model import Role


class UserCreate(BaseModel):
    nick_name: str = Field(min_length=2, max_length=50)
    password: str = Field(min_length=8)
    role: Role
    full_name: Optional[str] = None
    description_from_admin: Optional[str] = None


class UserRead(BaseModel):
    id: UUID
    nick_name: str
    role: Role
    full_name: Optional[str]
    description_from_admin: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    nick_name: Optional[str] = Field(None, min_length=2, max_length=50)
    password: Optional[str] = Field(None, min_length=8)
    role: Optional[str] = None
    full_name: Optional[str] = None
    description_from_admin: Optional[str] = None
