import enum
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class ReportExportParams(BaseModel):
    export_type: str
    start_date: date
    end_date: date
    user_id: int | None = None


class ReportExportResponse(ReportExportParams):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ReportStatus(enum.Enum):
    waiting = "waiting"
    in_progress = "in_progress"
    failed = "failed"
    completed = "completed"


class ReportExportRow(BaseModel):
    id: int
    start_time: datetime
    end_time: datetime
    status: str
    message: str
    user_full_name: str
    location_name: str
    location_address: str
    assignment_date: date
