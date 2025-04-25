from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.User.model import Role, UserStatus


# 📥 Используется ТОЛЬКО при регистрации
class RegisterUser(BaseModel):
    nickname: str = Field(min_length=2, max_length=50)
    password: str = Field(min_length=8)  # обычный пароль
    role: Optional[Role] = Role.employee
    full_name: Optional[str] = None
    admin_note: Optional[str] = None


# 📤 Используется для отправки данных в базу (уже с хэшем)
class UserCreate(BaseModel):
    nickname: str
    hashed_password: str  # уже захэширован
    role: Role
    status: UserStatus = UserStatus.pending
    full_name: Optional[str] = None
    admin_note: Optional[str] = None


class UserRead(BaseModel):
    id: int
    nickname: str
    role: Role
    status: UserStatus
    full_name: Optional[str]
    admin_note: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    nickname: Optional[str] = Field(None, min_length=2, max_length=50)
    hashed_password: Optional[str] = None  # если обновляем пароль — только хэш
    role: Optional[Role] = None
    status: Optional[UserStatus] = None
    full_name: Optional[str] = None
    admin_note: Optional[str] = None
