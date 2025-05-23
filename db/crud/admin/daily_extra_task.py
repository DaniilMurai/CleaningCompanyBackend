from sqlalchemy import select

from db.crud.models.daily_extra_task import DailyExtraTaskCRUD


class AdminDailyExtraTaskCRUD(DailyExtraTaskCRUD):

    async def get_daily_extra_task(self):
        daily_extra_task = await self.db.execute(select(DailyExtraTaskCRUD))
        return daily_extra_task.scalars().all()
