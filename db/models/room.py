from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from db.base import Base


class Room(Base):
    location_id = Column(ForeignKey("locations.id"), nullable=False)
    name = Column(String, nullable=False)

    location = relationship("Location", back_populates="rooms")
    room_tasks = relationship("RoomTask", back_populates="room")
    daily_extra_tasks = relationship("DailyExtraTask", back_populates="room")
