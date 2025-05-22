from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.base import Base


class RoomTask(Base):
    task_id = Column(ForeignKey("tasks.id"), nullable=False)
    room_id = Column(ForeignKey("rooms.id"), nullable=False)
    times_since_done = Column(Integer, default=0)

    task = relationship("Task", back_populates="room_tasks")
    room = relationship("Room", back_populates="room_tasks")
