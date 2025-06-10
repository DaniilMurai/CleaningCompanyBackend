from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, computed_field, field_validator

import exceptions
import schemas
from schemas import DailyAssignmentForUserResponse


class ReportBase(BaseModel):
    daily_assignment_id: int
    user_id: int
    message: Optional[str] = None
    media_links: Optional[list[str]] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: schemas.AssignmentStatus

    @field_validator("end_time")
    def validate_times(cls, end_time_value: Optional[datetime], info):
        """
        Этот валидатор срабатывает, когда Pydantic валидирует поле end_time.
        info.data — это словарь со значениями всех ранее провалидированных полей,
        то есть там уже может лежать start_time (если его передали).
        """
        start_time_value = info.data.get("start_time")

        # Если либо start_time, либо end_time не заданы, просто возвращаем end_time
        # без ошибок
        if start_time_value is None or end_time_value is None:
            return end_time_value

        # Если оба поля заданы, проверяем, что end_time > start_time
        if end_time_value <= start_time_value:
            raise exceptions.EndTimeMustBeAfterStartTime(
                {"start_time": start_time_value, "end_time": end_time_value}
            )

        return end_time_value


class CreateReport(ReportBase):
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

    @field_validator('end_time')
    def validate_update_times(cls, end_time, info):
        start_time = info.data.get('start_time')
        if start_time and end_time:
            if end_time <= start_time:
                raise exceptions.EndTimeMustBeAfterStartTime
        return end_time


class ReportResponse(ReportBase):
    """Схема для ответа API"""
    id: int

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
        # json_encoders удален - не нужен в Pydantic V2
    )


class AssignmentReportResponse(BaseModel):
    assignment: DailyAssignmentForUserResponse
    report: ReportResponse | None = None
