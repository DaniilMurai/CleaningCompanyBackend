from datetime import datetime

from pydantic import BaseModel


class AdminGetListParams(BaseModel):
    offset: int | None = None
    limit: int | None = None
    search: str | None = None


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


class RoomTaskCreate(BaseModel):
    room_id: int
    task_id: int


class RoomTaskUpdate(BaseModel):
    times_since_done: int | None = None
    room_id: int | None = None
    task_id: int | None = None


class RoomTaskResponse(BaseModel):
    id: int
    room_id: int
    task_id: int
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


class DailyAssignmentResponse(BaseModel):
    id: int
    location_id: int
    user_id: int
    date: datetime
    admin_note: str | None = None
    user_note: str | None = None

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
    admin_note: str | None = None
    user_note: str | None = None

    class Config:
        from_attributes = True


# class DailyAssignmentResponse(DailyAssignmentCreate):
#     id: int
#     user_note: str | None = None
#     admin_note: str | None = None
#     extra_tasks: list["DailyExtraTaskResponse"] = []
#     user: "UserResponse"
#     location: LocationResponse
#
#     class Config:
#         from_attributes = True


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

# class DailyExtraTaskResponse(DailyExtraTaskCreate):
#     id: int
#     room: RoomResponse
#     task: TaskResponse
#
#     class Config:
#         from_attributes = True


# class UserRole(enum.Enum):
#     employee = "employee"
#     admin = "admin"
#     superadmin = "superadmin"
#
#
# class UserStatus(enum.Enum):
#     pending = "pending"
#     active = "active"
#     disabled = "disabled"
#
#
# class UserResponse(BaseModel):
#     id: int
#     nickname: str
#     role: UserRole
#     status: UserStatus
#     full_name: Optional[str]
#     admin_note: Optional[str]
#     created_at: datetime
#
#     class Config:
#         from_attributes = True
