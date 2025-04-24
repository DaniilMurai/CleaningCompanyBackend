from fastapi import APIRouter

from app.router import health, admin

router = APIRouter()

router.include_router(health.router)
router.include_router(admin.router)
