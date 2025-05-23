from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends, Query

import schemas
from api.admin.router.daily_assignments.service import AdminDailyAssignmentService

router = APIRouter(prefix="/daily-assignments", tags=["daily-assignments"])


@router.get("/")
async def get_daily_assignments(
        params: Annotated[schemas.DailyAssignmentUpdate, Query()],
        service: AdminDailyAssignmentService = Depends()
) -> list[schemas.DailyAssignmentResponse]:
    return await service.get_daily_assignments(params)


@router.post("/")
async def create_daily_assignment(
        data: schemas.DailyAssignmentCreate,
        service: AdminDailyAssignmentService = Depends()
) -> schemas.DailyAssignmentResponse:
    return await service.create_daily_assignment(data)


@router.patch("/")
async def edit_daily_assignment(
        daily_assignment_id: int,
        data: schemas.DailyAssignmentUpdate,
        service: AdminDailyAssignmentService = Depends()
) -> schemas.DailyAssignmentResponse:
    return await service.update_daily_assignment(daily_assignment_id, data)


@router.delete("/")
async def delete_daily_assignment(
        daily_assignment_id: int,
        service: AdminDailyAssignmentService = Depends()
) -> schemas.SuccessResponse:
    return await service.delete_daily_assignment(daily_assignment_id)
