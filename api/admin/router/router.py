from fastapi import APIRouter

from . import locations, rooms, users

router = APIRouter()

router.include_router(users.router)
router.include_router(locations.router)
router.include_router(rooms.router)
