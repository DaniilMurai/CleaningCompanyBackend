import uuid
from datetime import date
from typing import Optional, Sequence

from sqlalchemy import and_, func, select, update
from sqlalchemy.exc import SQLAlchemyError

import exceptions
import schemas
from db.crud.models.daily_assignment import DailyAssignmentCRUD
from db.models import DailyAssignment, Report
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
            )
        else:
            daily_assignments = await self.db.execute(select(DailyAssignment))

        return daily_assignments.scalars().all()

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
            first = assignments[0]
            second = assignments[1]
            days_diff = (second.date - first.date).days
            return schemas.AssignmentGroup.model_validate(
                {"assignments_amount": len(assignments), "interval_days": days_diff}
            )

        return schemas.AssignmentGroup.model_validate(
            {{"assignments_amount": len(assignments), "interval_days": None}}
        )

    async def delete_daily_assignments_group(self, group_uuid: uuid.uuid4()):
        try:
            stmt = update(DailyAssignment).where(
                DailyAssignment.group_uuid == group_uuid
            ).values(is_deleted=True)
            await self.db.execute(stmt)
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e

    async def mark_expired_assignments_as_not_completed(self):
        today = date.today()

        conditions = and_(
            DailyAssignment.status == AssignmentStatus.not_started,
            DailyAssignment.date < today,
            DailyAssignment.is_deleted.is_(False)
        )

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
