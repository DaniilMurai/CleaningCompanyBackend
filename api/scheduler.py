# scheduler.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc

from db.crud.admin.daily_assignment import AdminDailyAssignmentCRUD
from db.session import async_session_maker


async def start_daily_assignment_scheduler():
    print("start_daily_assignment_scheduler")
    async with async_session_maker() as db:
        crud = AdminDailyAssignmentCRUD(db=db)
        scheduler = AsyncIOScheduler(timezone=utc)
        scheduler.add_job(
            crud.mark_expired_assignments_as_not_completed,
            'cron',
            hour=2, minute=1
        )
        scheduler.start()
