from enum import Enum
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


class SortDirection(str, Enum):
    asc = "asc"
    desc = "desc"


class UserFields(
    str, Enum
):  # Наследуемся от str для автоматического приведения к строке
    id = "id"  # ✅ Значение явно задано
    nickname = "nickname"
    role = "role"
    status = "status"
    full_name = "full_name"
    admin_note = "admin_note"
    created_at = "created_at"


class GetUsersParams(BaseModel):
    role: UserRole | None = None
    status: UserStatus | None = None
    nickname: str | None = None
    search: str | None = None
    offset: int | None = None
    limit: int | None = None
    order_by: UserFields | None = None  # Используем Enum напрямую
    direction: SortDirection | None = None  # Отдельный параметр для направления


class InviteLink(BaseModel):
    invite_link: str


class ForgetPasswordLink(BaseModel):
    forget_password_link: str
