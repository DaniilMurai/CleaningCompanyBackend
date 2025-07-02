from sqlalchemy import Column, Enum, ForeignKey
from sqlalchemy.orm import relationship

import schemas
from db.base import Base


class ReportRoom(Base):
    room_id = Column(ForeignKey("rooms.id"), nullable=False)
    report_id = Column(ForeignKey("reports.id"), nullable=False)
    status = Column(Enum(schemas.RoomStatus))

    rooms = relationship("Room", back_populates="report_rooms")
    reports = relationship("Report", back_populates="report_rooms")
