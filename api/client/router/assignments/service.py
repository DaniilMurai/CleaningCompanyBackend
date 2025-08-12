from datetime import date

from sqlalchemy import and_, func, select
from sqlalchemy.orm import selectinload

import exceptions
import schemas
from api.users.base.service import UserDepend
from db.crud import UserCRUD
from db.crud.models.daily_assignment import DailyAssignmentCRUD
from db.crud.models.daily_extra_task import DailyExtraTaskCRUD
from db.crud.models.location import LocationCRUD
from db.crud.models.room import RoomCRUD
from db.crud.models.room_task import RoomTaskCRUD
from db.crud.models.task import TaskCRUD
from db.models import DailyAssignment, Location, Report, Room, RoomTask
from utils.benchmark import benchmark


class AssignmentService:
    def __init__(
            self,
            user: UserDepend,
            crud: UserCRUD.depends(),
            daily_assignment_crud: DailyAssignmentCRUD.depends(),
            location_crud: LocationCRUD.depends(),
            room_crud: RoomCRUD.depends(),
            task_crud: TaskCRUD.depends(),
            room_task_crud: RoomTaskCRUD.depends(),
            daily_extra_task_crud: DailyExtraTaskCRUD.depends()
    ):
        self.user = user
        self.crud = crud
        self.daily_crud = daily_assignment_crud
        self.location_crud = location_crud
        self.room_crud = room_crud
        self.task_crud = task_crud
        self.room_task_crud = room_task_crud
        self.daily_extra_task_crud = daily_extra_task_crud

    async def get_daily_assignments_dates(self):
        assignment_dates = await self.daily_crud.db.execute(
            select(func.date(DailyAssignment.date)).distinct()
            .where(
                and_(
                    DailyAssignment.is_deleted == False,
                    DailyAssignment.user_id == self.user.id
                )
            )
            .order_by(func.date(DailyAssignment.date))

        )
        return assignment_dates.scalars().all()

    async def update_daily_assignment_status(
            self, assignment_id: int, status: schemas.AssignmentStatus
    ) -> schemas.DailyAssignmentForUserResponse:

        # Получаем чистую ORM-модель без дополнительных данных
        daily_assignment_orm = await self.daily_crud.get(
            id=assignment_id, user_id=self.user.id
        )

        if not daily_assignment_orm:
            raise exceptions.ObjectNotFoundByIdError("daily_assignment", assignment_id)

        # Обновляем только статус
        data = {"status": status}
        await self.daily_crud.update(daily_assignment_orm, data)

        # Теперь получаем полный объект через существующий метод
        # который загружает все связи и возвращает полную схему
        return await self.get_daily_assignment_by_id(assignment_id)

    async def get_daily_assignments_and_reports(
            self,
            params: schemas.AssignmentAndReportsParams | None = None
    ) -> list[schemas.AssignmentReportResponse]:
        dates = params.dates if params.dates else None
        assignments = await self.get_daily_assignments(dates)
        return await self.daily_crud.get_assignment_and_reports(assignments)

    async def update_daily_assignment(
            self, assignment_id: int, data: schemas.DailyAssignmentForUserUpdate
    ) -> schemas.DailyAssignmentForUserResponse:
        daily_assignment_orm = await self.daily_crud.get(
            id=assignment_id, user_id=self.user.id
        )
        if not daily_assignment_orm:
            raise exceptions.ObjectNotFoundByIdError("daily_assignment", assignment_id)
        data_to_update = data.model_dump(exclude_unset=True)
        await self.daily_crud.update(daily_assignment_orm, data_to_update)

        return await self.get_daily_assignment_by_id(assignment_id)

    @benchmark
    async def get_daily_assignment_by_id(
            self, assignment_id: int
    ) -> schemas.DailyAssignmentForUserResponse:

        d = (await self.daily_crud.db.execute(
            select(DailyAssignment)
            .where(
                DailyAssignment.id == assignment_id,
                DailyAssignment.is_deleted == False
            ).options(
                selectinload(DailyAssignment.location)
                .selectinload(Location.rooms)
                .selectinload(Room.room_tasks)
                .selectinload(RoomTask.task)
            )
        )).scalars().one_or_none()

        if not d:
            raise exceptions.ObjectNotFoundByIdError(
                "daily_assignment from user id", self.user.id
            )

        location_response = d.location
        rooms = d.location.rooms
        room_tasks = []
        tasks_dict = {}
        for r in rooms:
            for rt in r.room_tasks:
                room_tasks.append(rt)
                tasks_dict[rt.task_id] = rt.task

        tasks = list(tasks_dict.values())

        rooms_response = [schemas.RoomResponse.model_validate(r) for r in rooms]
        room_task_response = [schemas.RoomTaskResponse.model_validate(rt) for rt
                              in
                              room_tasks]
        tasks_response = [schemas.TaskResponse.model_validate(t) for t in tasks]

        det_rows = await self.daily_extra_task_crud.get_list_extra_tasks(d.id)

        assigned_tasks_response: list[schemas.DailyExtraTaskResponse] = []

        for det in det_rows:
            task_obj = det.task or await self.task_crud.get(det.task_id)
            room_obj = det.room or await self.room_crud.get(det.room_id)

            assigned_tasks_response.append(
                schemas.DailyExtraTaskResponse(
                    id=det.id,
                    task=schemas.TaskResponse.model_validate(
                        task_obj, from_attributes=True
                    ),
                    room=schemas.RoomResponse.model_validate(
                        room_obj, from_attributes=True
                    ),
                    completed=det.completed if hasattr(det, "completed") else None
                )
            )

        return schemas.DailyAssignmentForUserResponse(
            id=d.id,
            location=location_response,
            rooms=rooms_response,
            room_tasks=room_task_response,
            tasks=tasks_response,
            assigned_tasks=assigned_tasks_response,
            user_id=d.user_id,
            date=d.date,
            status=d.status,
            admin_note=d.admin_note,
            user_note=d.user_note,
            start_time=d.start_time,
            end_time=d.end_time
        )

    @benchmark
    async def get_daily_assignments(
            self, dates: list[date] | None = None
    ) -> list[schemas.DailyAssignmentForUserResponse]:

        if dates:
            daily_assignments = (await self.daily_crud.db.execute(
                select(DailyAssignment).where(
                    and_(
                        DailyAssignment.is_deleted == False,
                        func.date(DailyAssignment.date).in_(dates),
                        DailyAssignment.user_id == self.user.id
                    )
                ).options(
                    selectinload(DailyAssignment.location)
                    .selectinload(Location.rooms)
                    .selectinload(Room.room_tasks)
                    .selectinload(RoomTask.task)
                )
            )).scalars().all()
        else:

            daily_assignments = (await self.daily_crud.db.execute(
                select(DailyAssignment).where(
                    and_(
                        DailyAssignment.is_deleted == False,
                        DailyAssignment.user_id == self.user.id
                    )
                ).options(
                    selectinload(DailyAssignment.location)
                    .selectinload(Location.rooms)
                    .selectinload(Room.room_tasks)
                    .selectinload(RoomTask.task)
                )
            )).scalars().all()

        result = []

        for d in daily_assignments:
            location_response = d.location

            rooms = d.location.rooms
            room_tasks = []
            tasks_dict = {}
            for r in rooms:
                for rt in r.room_tasks:
                    room_tasks.append(rt)
                    tasks_dict[rt.task_id] = rt.task

            tasks = list(tasks_dict.values())

            rooms_response = [schemas.RoomResponse.model_validate(r) for r in rooms]
            room_task_response = [schemas.RoomTaskResponse.model_validate(rt) for rt
                                  in
                                  room_tasks]
            tasks_response = [schemas.TaskResponse.model_validate(t) for t in tasks]

            det_rows = await self.daily_extra_task_crud.get_list_extra_tasks(d.id)

            assigned_tasks_response: list[schemas.DailyExtraTaskResponse] = []

            for det in det_rows:
                task_obj = det.task or await self.task_crud.get(det.task_id)
                room_obj = det.room or await self.room_crud.get(det.room_id)

                assigned_tasks_response.append(
                    schemas.DailyExtraTaskResponse(
                        id=det.id,
                        task=schemas.TaskResponse.model_validate(
                            task_obj, from_attributes=True
                        ),
                        room=schemas.RoomResponse.model_validate(
                            room_obj, from_attributes=True
                        ),
                        completed=det.completed if hasattr(det, "completed") else None
                    )
                )

            result.append(
                schemas.DailyAssignmentForUserResponse(
                    id=d.id,
                    location=location_response,
                    rooms=rooms_response,
                    assigned_tasks=assigned_tasks_response,
                    room_tasks=room_task_response,
                    tasks=tasks_response,
                    user_id=d.user_id,
                    date=d.date,
                    status=d.status,
                    admin_note=d.admin_note,
                    user_note=d.user_note,
                    start_time=d.start_time,
                    end_time=d.end_time
                )
            )

        return result

    async def get_daily_assignment_and_report_by_report_id(
            self, report_id: int
    ) -> schemas.AssignmentReportResponse:
        report = await self.crud.get(report_id, Report)
        if not report:
            raise exceptions.ObjectNotFoundByIdError("report", report_id)

        assignment = await self.get_daily_assignment_by_id(report.daily_assignment_id)

        if not assignment:
            raise exceptions.ObjectNotFoundByIdError(
                "assignment by report id", report_id
            )
        assignment_schema = schemas.DailyAssignmentForUserResponse.model_validate(
            assignment
        )
        report_schema = schemas.ReportResponse.model_validate(
            report
        )

        return schemas.AssignmentReportResponse(
            assignment=assignment_schema,
            report=report_schema,
        )
