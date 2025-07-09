from datetime import date
from typing import Optional, Sequence

from sqlalchemy import func, select, update

from db.crud.models.daily_assignment import DailyAssignmentCRUD
from db.models import DailyAssignment
from schemas import AssignmentStatus


class AdminDailyAssignmentCRUD(DailyAssignmentCRUD):

    async def get_daily_assignments(self, dates: Optional[list[date]] = None) -> \
            Sequence[DailyAssignment]:
        if dates:
            daily_assignments = await self.db.execute(
                select(DailyAssignment).where(
                    func.date(DailyAssignment.date).in_(dates)
                )
            )
        else:
            daily_assignments = await self.db.execute(select(DailyAssignment))

        return daily_assignments.scalars().all()

    async def mark_expired_assignments_as_not_completed(self):
        today = date.today()
        print("mark_expired_assignments_as_not_completed")
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
