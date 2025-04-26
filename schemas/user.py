import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserRole(enum.Enum):
    employee = "employee"
    admin = "admin"
    superadmin = "superadmin"


class UserStatus(enum.Enum):
    pending = "pending"
    active = "active"
    disabled = "disabled"


# 📥 Используется ТОЛЬКО при регистрации
class RegisterUserData(BaseModel):
    nickname: str = Field(min_length=2, max_length=50)
    password: str = Field(min_length=8)  # обычный пароль
    role: Optional[UserRole] = UserRole.employee
    full_name: Optional[str] = None
    admin_note: Optional[str] = None


# 📤 Используется для отправки данных в базу (уже с хэшем)
class UserCreate(BaseModel):
    nickname: str
    hashed_password: str  # уже захэширован
    role: UserRole
    status: UserStatus = UserStatus.pending
    full_name: Optional[str] = None
    admin_note: Optional[str] = None


class UserRead(BaseModel):
    id: int
    nickname: str
    role: UserRole
    status: UserStatus
    full_name: Optional[str]
    admin_note: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdateData(BaseModel):
    nickname: Optional[str] = Field(None, min_length=2, max_length=50)
    password: Optional[str] = None
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None
    full_name: Optional[str] = None
    admin_note: Optional[str] = None
