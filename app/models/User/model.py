import enum
from datetime import datetime

from sqlalchemy import (Column, DateTime, Enum as SQLEnum, Integer, String)

from app.db.base import Base


class Role(enum.Enum):
    employee = "employee"
    admin = "admin"
    superadmin = "superadmin"


class UserStatus(enum.Enum):
    pending = "pending"
    active = "active"
    disabled = "disabled"


class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(Role), default=Role.employee, nullable=False)
    status = Column(SQLEnum(UserStatus), default=UserStatus.pending, nullable=False)
    full_name = Column(String)
    admin_note = Column(String)
    created_at = Column(DateTime, default=datetime.now())
