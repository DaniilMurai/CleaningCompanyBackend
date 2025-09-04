from sqlalchemy import Column, Integer, String, and_
from sqlalchemy.orm import relationship

from db.base import Base
from db.models import Hint, Inventory


class Task(Base):
    title = Column(String, nullable=False)
    description = Column(String)
    frequency = Column(Integer, nullable=False)  # Частота в днях

    room_tasks = relationship("RoomTask", back_populates="task")
    daily_extra_tasks = relationship("DailyExtraTask", back_populates="task")
    hints = relationship(
        "Hint", back_populates="task",
        primaryjoin=lambda: and_(Hint.task_id == Task.id, Hint.is_deleted == False)
    )
    inventory = relationship(
        "Inventory", back_populates="task", primaryjoin=lambda: and_(
            Inventory.task_id == Task.id, Inventory.is_deleted == False
        )
    )
