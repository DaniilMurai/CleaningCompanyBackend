import enum
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, computed_field, field_validator

import exceptions
import schemas
from schemas import (
    AdminGetListParams, DailyAssignmentForUserResponse,
    DailyAssignmentForUserWithHintsResponse,
)


class AdminReportFilterParams(AdminGetListParams):
    status: Optional[str] = None


class RoomStatus(enum.Enum):
    not_done = "not_done"
    done = "done"
    partially_done = "partially_done"


class ReportRoomResponse(BaseModel):
    room_id: int
    report_id: int
    status: RoomStatus


class ReportRoomRequest(BaseModel):
    room_id: int
    status: RoomStatus


class TimeValidatedReportBase(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    @field_validator("end_time")
    def validate_times(cls, end_time_value: Optional[datetime], info):
        start_time_value = info.data.get("start_time")
        if start_time_value is None or end_time_value is None:
            return end_time_value
        if end_time_value <= start_time_value:
            raise exceptions.EndTimeMustBeAfterStartTime(
                {"start_time": start_time_value, "end_time": end_time_value}
            )
        return end_time_value


class ReportBase(TimeValidatedReportBase):
    daily_assignment_id: int
    user_id: int
    message: Optional[str] = None
    media_links: Optional[list[str]] = None
    status: schemas.AssignmentStatus


class CreateReport(ReportBase):
    report_rooms: Optional[list[ReportRoomRequest]] = None
    pass


class UpdateReport(BaseModel):
    """Схема для обновления отчета"""
    # __annotations__ = {k: Optional[v] for k, v in ReportBase.__annotations__.items()}

    daily_assignment_id: Optional[int] = None
    user_id: Optional[int] = None
    message: Optional[str] = None
    media_links: Optional[list[str]] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[schemas.AssignmentStatus] = None
    report_rooms: Optional[list[ReportRoomRequest]] = None

    @field_validator('end_time')
    def validate_update_times(cls, end_time, info):
        start_time = info.data.get('start_time')
        if start_time and end_time:
            if end_time <= start_time:
                raise exceptions.EndTimeMustBeAfterStartTime
        return end_time


class ReportResponse(TimeValidatedReportBase):
    """Схема для ответа API"""
    id: int
    daily_assignment_id: int  # Legacy
    user_id: int  # Legacy
    location_name: Optional[str] = None
    user_full_name: Optional[str] = None
    report_rooms: Optional[list[ReportRoomResponse]] = []
    message: Optional[str] = None
    media_links: Optional[list[str]] = None
    status: schemas.AssignmentStatus

    # Убираем явные декларации duration_seconds и duration_minutes
    # Они будут полностью вычисляемыми

    @computed_field
    @property
    def duration_seconds(self) -> float | None:
        """Вычисляет длительность в секундах"""
        if self.start_time is None or self.end_time is None:
            return None
        return (self.end_time - self.start_time).total_seconds()

    @computed_field
    @property
    def duration_minutes(self) -> float | None:
        """Возвращает длительность в минутах"""
        if self.start_time is None or self.end_time is None:
            return None
        return round(self.duration_seconds / 60, 1)

    @computed_field
    @property
    def duration_hours(self) -> float | None:
        """Возвращает длительность в часах"""
        if self.start_time is None or self.end_time is None:
            return None
        return round(self.duration_seconds / 3600, 2)

    # Конфигурация для работы с ORM
    model_config = ConfigDict(
        from_attributes=True,
    )


class ReportWithAssignmentDateResponse(ReportResponse):
    assignment_date: Optional[date]


class AssignmentWithHintsReportResponse(BaseModel):
    assignment: DailyAssignmentForUserWithHintsResponse
    report: ReportResponse | None = None


class AssignmentReportResponse(BaseModel):
    assignment: DailyAssignmentForUserResponse
    report: ReportResponse | None = None


class AssignmentAndReportsParams(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    dates: Optional[list[date]] = None
