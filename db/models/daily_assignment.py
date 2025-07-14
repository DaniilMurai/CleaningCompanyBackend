from datetime import timedelta

from sqlalchemy import (
    Column, ColumnElement, Date, Enum, ForeignKey, String,
    TIMESTAMP, func,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

import schemas
from db.base import Base


class DailyAssignment(Base):
    location_id = Column(ForeignKey("locations.id"), nullable=False)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    admin_note = Column(String)
    user_note = Column(String)
    start_time = Column(TIMESTAMP(timezone=True))
    end_time = Column(TIMESTAMP(timezone=True))
    status = Column(
        Enum(schemas.AssignmentStatus),
        server_default=schemas.AssignmentStatus.not_started.value,
        default=schemas.AssignmentStatus.not_started,
        nullable=False,
    )

    location = relationship("Location", back_populates="daily_assignments")
    user = relationship("User", back_populates="daily_assignments")
    daily_extra_tasks = relationship(
        "DailyExtraTask", back_populates="daily_assignment"
    )
    reports = relationship(
        "Report", back_populates="daily_assignment"
    )

    @hybrid_property
    def duration(self) -> timedelta:
        if self.end_time and self.start_time:
            return self.end_time - self.start_time
        return timedelta(0)

    @duration.expression
    def duration(cls) -> ColumnElement[timedelta]:
        return func.age(cls.end_time - cls.start_time)
