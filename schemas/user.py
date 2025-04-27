import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserRole(enum.Enum):
    employee = "employee"
    admin = "admin"
    superadmin = "superadmin"


class UserStatus(enum.Enum):
    pending = "pending"
    active = "active"
    disabled = "disabled"


class UserUpdatePassword(BaseModel):
    old_password: str
    new_password: str


class UserSchema(BaseModel):
    id: int
    nickname: str
    role: UserRole
    status: UserStatus
    full_name: Optional[str]
    admin_note: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class UpdateUserData(BaseModel):
    nickname: Optional[str] = None
    full_name: Optional[str] = None
