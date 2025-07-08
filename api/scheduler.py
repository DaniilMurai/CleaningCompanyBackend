# scheduler.py
import asyncio

from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc

from db.crud.admin.daily_assignment import AdminDailyAssignmentCRUD
from db.session import async_session_maker


def start_daily_assignment_scheduler():
    with async_session_maker() as db:
        crud = AdminDailyAssignmentCRUD(db=db)
        scheduler = BackgroundScheduler(timezone=utc)
        scheduler.add_job(
            lambda: asyncio.run(crud.mark_expired_assignments_as_not_completed()),
            'cron',
            hour=0, minute=1
        )
        scheduler.start()
