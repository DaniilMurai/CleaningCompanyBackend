import enum
from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    Column, String, Enum as SQLEnum, DateTime
)
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base


class Role(enum.Enum):
    employee = "employee"
    admin = "admin"
    superadmin = "superadmin"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    nick_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(Role), default=Role.employee, nullable=False)
    full_name = Column(String)
    description_from_admin = Column(String)
    created_at = Column(DateTime, default=datetime.now())
