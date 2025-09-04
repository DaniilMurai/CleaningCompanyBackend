from fastapi import APIRouter

from . import (
    daily_assignments, daily_extra_tasks, export_reports, hints, inventories,
    inventory_users, locations, reports, room_tasks, rooms, tasks, users,
)

router = APIRouter()

router.include_router(users.router)
router.include_router(locations.router)
router.include_router(rooms.router)
router.include_router(tasks.router)
router.include_router(room_tasks.router)
router.include_router(daily_assignments.router)
router.include_router(daily_extra_tasks.router)
router.include_router(reports.router)
router.include_router(export_reports.router)
router.include_router(hints.router)
router.include_router(inventories.router)
router.include_router(inventory_users.router)
