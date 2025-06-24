# scheduler.py
import asyncio

from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc

from db.crud.admin.daily_assignment import AdminDailyAssignmentCRUD


def start_daily_assignment_scheduler():
    crud = AdminDailyAssignmentCRUD(...)
    scheduler = BackgroundScheduler(timezone=utc)
    scheduler.add_job(
        lambda: asyncio.run(crud.mark_expired_assignments_as_not_completed()),
        'cron',
        hour=0, minute=1
    )
    scheduler.start()
