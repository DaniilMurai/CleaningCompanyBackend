from sqlalchemy import Column, DateTime, Enum, ForeignKey, String, TIMESTAMP
from sqlalchemy.orm import relationship

import schemas
from db.base import Base


class DailyAssignment(Base):
    location_id = Column(ForeignKey("locations.id"), nullable=False)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
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
