from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from db.base import Base


class Location(Base):
    name = Column(String, nullable=False)
    address = Column(String)

    rooms = relationship("Room", back_populates="location")
    daily_assignments = relationship("DailyAssignment", back_populates="location")
