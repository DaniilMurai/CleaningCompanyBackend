from datetime import date

from sqlalchemy import select, update

from db.crud.models.daily_assignment import DailyAssignmentCRUD
from db.models import DailyAssignment
from schemas import AssignmentStatus


class AdminDailyAssignmentCRUD(DailyAssignmentCRUD):

    async def get_daily_assignments(self):
        daily_assignment = await self.db.execute(select(DailyAssignment))
        return daily_assignment.scalars().all()

    async def mark_expired_assignments_as_not_completed(self):
        today = date.today()

        stmt = (update(DailyAssignment)
                .where(
            DailyAssignment.status == AssignmentStatus.not_started,
            DailyAssignment.date < today,
            DailyAssignment.is_deleted.is_(False)
        )
                .values(status=AssignmentStatus.expired)
                )

        await self.db.execute(stmt)
        await self.db.commit()
