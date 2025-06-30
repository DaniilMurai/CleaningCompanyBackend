import enum
from datetime import date, datetime, timedelta
from typing import Optional

from pydantic import BaseModel, ConfigDict, computed_field, model_validator

import schemas


class ReportExportParams(BaseModel):
    export_type: str
    start_date: date
    end_date: date
    timezone: str
    user_id: int | None = None
    lang: Optional[str] = "ru"


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
    start_time: datetime | None = None
    end_time: datetime | None = None
    start_time_str: str | None = None
    end_time_str: str | None = None
    status: str
    message: str | None = None
    user_full_name: str
    location_name: str
    location_address: str | None = None
    assignment_date: date

    # rooms: list[schemas.ReportRoom] = []
    #
    # @computed_field
    # @property
    # def failed_rooms(self) -> list[schemas.ReportRoom]:
    #     return [room for room in self.rooms if room.status != RoomStatus.done]

    @model_validator(mode="after")
    def compute_human_time(self):
        self.start_time_str = self.start_time.strftime("%H:%M")
        self.end_time_str = self.end_time.strftime("%H:%M")
        return self

    @computed_field
    def duration(self) -> timedelta:
        return self.end_time - self.start_time


class RoomStatus(enum.Enum):
    not_done = "not_done"
    done = "done"
    partially_done = "partially_done"


class ReportRoom:
    room_id: int
    report_id: int
    status: schemas.RoomStatus
