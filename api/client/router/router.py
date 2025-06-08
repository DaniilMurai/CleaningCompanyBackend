from fastapi import APIRouter

from . import (assignments, reports)

router = APIRouter()

router.include_router(assignments.router)
router.include_router(reports.router)
