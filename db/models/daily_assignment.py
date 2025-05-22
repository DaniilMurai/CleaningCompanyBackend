from sqlalchemy import Column, Date, ForeignKey, String
from sqlalchemy.orm import relationship

from db.base import Base


class DailyAssignment(Base):
    location_id = Column(ForeignKey("locations.id"), nullable=False)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    admin_note = Column(String)
    user_note = Column(String)

    location = relationship("Location", back_populates="daily_assignments")
    user = relationship("User", back_populates="daily_assignments")
    daily_extra_tasks = relationship(
        "DailyExtraTask", back_populates="daily_assignment"
    )
