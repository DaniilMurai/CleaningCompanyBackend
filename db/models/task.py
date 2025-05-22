from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.base import Base


class Task(Base):
    title = Column(String, nullable=False)
    description = Column(String)
    frequency = Column(Integer, nullable=False)  # Частота в днях

    room_tasks = relationship("RoomTask", back_populates="task")
    daily_extra_tasks = relationship("DailyExtraTask", back_populates="task")
