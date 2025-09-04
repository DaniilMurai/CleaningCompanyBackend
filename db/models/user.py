from datetime import datetime

from sqlalchemy import (Column, DateTime, Enum as SQLEnum, String)
from sqlalchemy.orm import relationship

import schemas
from utils.date_time import utcnow
from ..base import Base


class User(Base):
    nickname: str | None = Column(String, unique=True)
    hashed_password: str | None = Column(String)
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
    full_name: str = Column(String, nullable=False)
    admin_note: str | None = Column(String)
    created_at: datetime = Column(
        DateTime(timezone=True),
        default=lambda: utcnow(),
        nullable=False,
    )

    daily_assignments = relationship("DailyAssignment", back_populates="user")
    # Обратная связь для отчетов
    reports = relationship(
        "Report", back_populates="user",
    )
    reports_exports = relationship("ReportsExport", back_populates="user")
    inventory_users = relationship("InventoryUser", back_populates="user")

    @property
    def allowed_scopes(self):
        # creating a list of roles from enum members
        scopes = [el.value for el in schemas.UserRole]

        # returning all roles before and including current role position in list
        return scopes[:scopes.index(self.role.value) + 1]
