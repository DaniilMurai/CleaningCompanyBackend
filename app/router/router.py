from fastapi import APIRouter

from app.router import health

router = APIRouter()

router.include_router(health.router)
