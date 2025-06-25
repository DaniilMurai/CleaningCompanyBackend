import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, computed_field


class AdminGetListParams(BaseModel):
    offset: int | None = None
    limit: int | None = None
    search: str | None = None
    order_by: str | None = None
    direction: str | None = None


class LocationCreate(BaseModel):
    name: str
    address: str | None = None


class LocationUpdate(BaseModel):
    name: str | None = None
    address: str | None = None


class LocationResponse(BaseModel):
    id: int
    name: str
    address: str

    class Config:
        from_attributes = True


# class LocationResponse(LocationCreate):
#     id: int
#     rooms: list["RoomResponse"] = []
#
#     class Config:
#         from_attributes = True


class RoomCreate(BaseModel):
    name: str
    location_id: int


class RoomUpdate(BaseModel):
    name: str | None = None
    location_id: int | None = None


class RoomResponse(BaseModel):
    id: int
    name: str
    location_id: int

    class Config:
        from_attributes = True


#
# class RoomResponse(RoomCreate):
#     id: int
#     tasks: list["TaskResponse"] = []
#     location: LocationResponse
#
#     class Config:
#         from_attributes = True


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    frequency: int  # в днях


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    frequency: int | None = None


class TaskResponse(TaskCreate):
    id: int

    class Config:
        from_attributes = True


# class TaskResponse(TaskCreate):
#     id: int
#     rooms: list["RoomResponse"] = []
#
#     class Config:
#         from_attributes = True


class BaseRoomTask(BaseModel):
    room_id: int
    task_id: int


class RoomTaskCreate(BaseRoomTask):
    pass


class RoomTaskUpdate(BaseRoomTask):
    __annotations__ = {k: Optional[v] for k, v in BaseRoomTask.__annotations__.items()}
    times_since_done: int | None = None


class RoomTaskResponse(BaseRoomTask):
    id: int
    times_since_done: int

    class Config:
        from_attributes = True


# class RoomTaskResponse(RoomTaskCreate):
#     id: int
#     times_since_done: int
#     task: TaskResponse
#     room: RoomResponse
#
#     class Config:
#         from_attributes = True


class AssignmentStatus(enum.Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    partially_completed = "partially_completed"
    completed = "completed"
    not_completed = "not_completed"
    expired = "expired"


class DailyAssignmentCreate(BaseModel):
    location_id: int
    user_id: int
    date: datetime
    admin_note: str | None = None


class DailyAssignmentUpdate(BaseModel):
    location_id: int | None = None
    user_id: int | None = None
    date: datetime | None = None
    admin_note: str | None = None
    user_note: str | None = None


class DailyAssignmentForUserUpdate(BaseModel):
    start_time: datetime | None = None
    end_time: datetime | None = None
    status: AssignmentStatus | None = None


class DailyAssignmentResponse(BaseModel):
    id: int
    location_id: int
    user_id: int
    date: datetime
    admin_note: str | None = None
    user_note: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None

    class Config:
        from_attributes = True


class DailyAssignmentForUserResponse(BaseModel):
    id: int
    location: LocationResponse
    rooms: list[RoomResponse] = []
    tasks: list[TaskResponse] = []
    room_tasks: list[RoomTaskResponse] = []
    user_id: int
    date: datetime
    status: AssignmentStatus
    admin_note: str | None = None
    user_note: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None

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

    class Config:
        from_attributes = True


class DailyExtraTaskCreate(BaseModel):
    daily_assignment_id: int
    room_id: int
    task_id: int


class DailyExtraTaskUpdate(BaseModel):
    daily_assignment_id: int | None = None
    room_id: int | None = None
    task_id: int | None = None


class DailyExtraTaskResponse(BaseModel):
    id: int
    daily_assignment_id: int
    room_id: int
    task_id: int

    class Config:
        from_attributes = True
