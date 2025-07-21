from datetime import date
from typing import Optional, Sequence

from sqlalchemy import and_, func, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

import exceptions
import schemas
from db.crud.models.daily_assignment import DailyAssignmentCRUD
from db.models import DailyAssignment, DailyExtraTask, Report, Room, RoomTask
from schemas import AssignmentStatus


class AdminDailyAssignmentCRUD(DailyAssignmentCRUD):

    async def get_daily_assignments(self, dates: Optional[list[date]] = None) -> \
            Sequence[DailyAssignment]:
        if dates:
            daily_assignments = await self.db.execute(
                select(DailyAssignment).where(
                    and_(
                        func.date(DailyAssignment.date).in_(dates),
                        DailyAssignment.is_deleted == False
                    )
                )
                # .options(
                #     selectinload(DailyAssignment.user),
                #     selectinload(DailyAssignment.location)
                # )
            )
        else:
            daily_assignments = await self.db.execute(
                select(DailyAssignment)
                .where(
                    DailyAssignment.is_deleted == False
                )
                # .options(
                #     selectinload(DailyAssignment.user),
                #     selectinload(DailyAssignment.location)
                # )
            )

        return daily_assignments.scalars().all()

    async def create_daily_assignments_batch(
            self, data: list[schemas.DailyAssignmentCreate]
    ):
        daily_assignments = await self.create_batch(
            [item.model_dump() for item in data]
        )
        for d in daily_assignments:
            rooms = await self.db.execute(
                select(Room).where(Room.location_id == d.location_id)
            )
            rooms = rooms.scalars().all()
            room_ids = [room.id for room in rooms]

            room_tasks = await self.db.execute(
                select(RoomTask)
                .where(RoomTask.room_id.in_(room_ids))
                .options(selectinload(RoomTask.task))
            )

            room_tasks = room_tasks.scalars().all()

            daily_extra_tasks = []
            for rt in room_tasks:
                frequency = rt.task.frequency or 1
                if rt.times_since_done >= frequency:
                    daily_extra_tasks.append(
                        DailyExtraTask(
                            daily_assignment_id=d.id,
                            room_id=rt.room_id,
                            task_id=rt.task_id
                        )
                    )
                    rt.times_since_done = 1
                else:
                    rt.times_since_done += 1

            self.db.add_all(daily_extra_tasks)

        await self.db.commit()
        return daily_assignments

    async def check_assignment_group(
            self, daily_assignments_id: int
    ) -> schemas.AssignmentGroup:
        assignment = await self.get(daily_assignments_id)
        if not assignment:
            raise exceptions.ObjectNotFoundByIdError("assignment", daily_assignments_id)
        stmt = select(self.model).where(
            and_(
                self.model.is_deleted == False,
                self.model.group_uuid == assignment.group_uuid,
                self.model.date >= assignment.date
            )
        ).order_by(self.model.date)
        assignments = (await self.db.execute(stmt)).scalars().all()

        if len(assignments) >= 2:

            min_interval = min(
                (assignments[i + 1].date - assignments[i].date).days for i in
                range(len(assignments) - 1)
            )

            return schemas.AssignmentGroup.model_validate(
                {"assignments_amount": len(assignments), "interval_days": min_interval}
            )

        return schemas.AssignmentGroup.model_validate(
            {"assignments_amount": len(assignments), "interval_days": None}
        )

    async def delete_daily_assignments_group(self, assignment: DailyAssignment):
        try:
            stmt = update(DailyAssignment).where(
                and_(
                    DailyAssignment.group_uuid == assignment.group_uuid,
                    DailyAssignment.date >= assignment.date
                )
            ).values(is_deleted=True)
            await self.db.execute(stmt)
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e

    async def mark_expired_assignments_as_not_completed(self):
        today = date.today()

        print("mark_expired_assignments_as_not_completed")
        assignment_stmt = (update(DailyAssignment)
                           .where(
            and_(
                DailyAssignment.status == AssignmentStatus.not_started,
                DailyAssignment.date < today,
                DailyAssignment.is_deleted.is_(False)
            )
        )
                           .values(status=AssignmentStatus.expired)
                           .execution_options(synchronize_session="fetch")
                           )

        report_stmt = (update(Report)
                       .where(
            and_(
                Report.daily_assignment_id.in_(
                    select(DailyAssignment.id).where(
                        DailyAssignment.status == AssignmentStatus.expired,
                        DailyAssignment.date < today,
                        DailyAssignment.is_deleted.is_(False)
                    )
                ), Report.status != AssignmentStatus.expired
            )
        ).values(status=AssignmentStatus.expired)
                       .execution_options(synchronize_session="fetch")
                       )

        await self.db.execute(assignment_stmt)
        await self.db.execute(report_stmt)
        await self.db.commit()
