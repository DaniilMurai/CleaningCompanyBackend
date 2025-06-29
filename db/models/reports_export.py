from sqlalchemy import Column, Date, Enum, ForeignKey, String
from sqlalchemy.orm import relationship

import schemas
from db.base import Base


class ReportsExport(Base):
    export_type = Column(String, nullable=False)
    start_date = Column(Date(), nullable=False)
    end_date = Column(Date(), nullable=False)
    status = Column(
        Enum(schemas.ReportStatus),
        server_default=schemas.ReportStatus.waiting.value,
        default=schemas.ReportStatus.waiting,
        nullable=False
    )
    file_path = Column(String)
    timezone = Column(String)
    lang = Column(String)
    user_id = Column(ForeignKey("users.id"))

    user = relationship("User", back_populates="reports_exports")
