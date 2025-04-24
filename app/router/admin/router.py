from fastapi import APIRouter

from app.router.admin import users

router = APIRouter(prefix="/admin", tags=["admin"])

router.include_router(users.router)
