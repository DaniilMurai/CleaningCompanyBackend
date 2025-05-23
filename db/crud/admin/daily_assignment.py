from sqlalchemy import select

from db.crud.models.daily_assignment import DailyAssignmentCRUD
from db.models import DailyAssignment


class AdminDailyAssignmentCRUD(DailyAssignmentCRUD):

    async def get_daily_assignments(self):
        daily_assignment = await self.db.execute(select(DailyAssignment))
        return daily_assignment.scalars().all()
