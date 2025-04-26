from datetime import datetime

from sqlalchemy import (Column, DateTime, Enum as SQLEnum, String)

import schemas
from ..base import Base


class User(Base):
    nickname: str = Column(String, nullable=False)
    hashed_password: str = Column(String, nullable=False)
    role: schemas.UserRole = Column(
        SQLEnum(schemas.UserRole),
        default=schemas.UserRole.employee,
        nullable=False,
    )
    status: schemas.UserStatus = Column(
        SQLEnum(schemas.UserStatus),
        default=schemas.UserStatus.pending,
        nullable=False,
    )
    full_name: str | None = Column(String)
    admin_note: str | None = Column(String)
    created_at: datetime = Column(
        DateTime,
        default=datetime.now(),
        nullable=False,
    )

    @property
    def allowed_scopes(self):
        # creating a list of roles from enum members
        scopes = [el.value for el in schemas.UserRole]

        # returning all roles before and including current role position in list
        return scopes[:scopes.index(self.role.value) + 1]
