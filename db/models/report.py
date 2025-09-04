from datetime import timedelta

from sqlalchemy import (
    ARRAY, Column, ColumnElement, Enum, ForeignKey, String,
    TIMESTAMP, func,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

import schemas
from db.base import Base


class Report(Base):
    daily_assignment_id = Column(ForeignKey("daily_assignments.id"), nullable=False)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    message = Column(String)
    media_links = Column(ARRAY(String))
    start_time = Column(TIMESTAMP(timezone=True))
    end_time = Column(TIMESTAMP(timezone=True))
    status = Column(
        Enum(schemas.AssignmentStatus),
        nullable=False,
        server_default=schemas.AssignmentStatus.not_started.value
    )
    daily_assignment = relationship("DailyAssignment", back_populates="reports")
    user = relationship("User", back_populates="reports")
    report_rooms = relationship("ReportRoom", back_populates="reports")
    inventory_users = relationship("InventoryUser", back_populates="report")
    
    @hybrid_property
    def duration(self) -> timedelta:
        if self.end_time and self.start_time:
            return self.end_time - self.start_time
        return timedelta(0)

    @duration.expression
    def duration(cls) -> ColumnElement[timedelta]:
        return func.age(cls.end_time - cls.start_time)
