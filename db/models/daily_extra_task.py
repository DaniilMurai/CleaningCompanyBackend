from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base


class DailyExtraTask(Base):
    room_id = Column(ForeignKey("rooms.id"), nullable=False)
    daily_assignment_id = Column(ForeignKey("daily_assignments.id"), nullable=False)
    task_id = Column(ForeignKey("tasks.id"), nullable=False)

    room = relationship("Room", back_populates="daily_extra_tasks")
    daily_assignment = relationship(
        "DailyAssignment", back_populates="daily_extra_tasks"
    )
    task = relationship("Task", back_populates="daily_extra_tasks")
