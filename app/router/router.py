from fastapi import APIRouter

from app.router import admin, auth, health

router = APIRouter()

router.include_router(health.router)
router.include_router(admin.router)
router.include_router(auth.router)
