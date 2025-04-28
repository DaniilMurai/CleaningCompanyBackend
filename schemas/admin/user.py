from typing import Optional

from pydantic import BaseModel, Field

from ..user import UserRole, UserStatus


# 📥 Используется ТОЛЬКО при регистрации
class RegisterUserData(BaseModel):
    full_name: str
    role: Optional[UserRole] = UserRole.employee
    admin_note: Optional[str] = None


# 📤 Используется для отправки данных в базу (уже с хэшем)
class UserCreate(BaseModel):
    nickname: str
    hashed_password: str  # уже захэширован
    role: UserRole
    status: UserStatus = UserStatus.pending
    full_name: Optional[str] = None
    admin_note: Optional[str] = None


class UserUpdateData(BaseModel):
    nickname: Optional[str] = Field(None, min_length=2, max_length=50)
    password: Optional[str] = None
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None
    full_name: Optional[str] = None
    admin_note: Optional[str] = None


class GetUsersParams(BaseModel):
    role: UserRole | None = None
    status: UserStatus | None = None
    nickname: str | None = None
    search: str | None = None
    offset: int | None = None
    limit: int | None = None


class InviteLink(BaseModel):
    invite_link: str
