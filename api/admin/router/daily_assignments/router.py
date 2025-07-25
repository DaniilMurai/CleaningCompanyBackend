from datetime import date
from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends, Query

import schemas
from api.admin.router.daily_assignments.service import AdminDailyAssignmentService

router = APIRouter(prefix="/daily-assignments", tags=["daily assignments"])


@router.get("/")
async def get_daily_assignments(
        params: Annotated[schemas.AdminAssignmentDatesGetListParams, Query()],
        service: AdminDailyAssignmentService = Depends()
) -> list[schemas.DailyAssignmentWithLocationAndUserResponse]:
    return await service.get_daily_assignments(params)


@router.get("/dates")
async def get_daily_assignments_dates(
        service: AdminDailyAssignmentService = Depends()
) -> list[date]:
    return await service.get_daily_assignments_dates()


@router.get("/check-group")
async def check_assignment_group(
        daily_assignment_id: int,
        service: AdminDailyAssignmentService = Depends()
) -> schemas.AssignmentGroup:
    return await service.check_assignment_group(daily_assignment_id)


@router.post("/")
async def create_daily_assignment(
        data: schemas.DailyAssignmentCreate,
        service: AdminDailyAssignmentService = Depends()
) -> schemas.DailyAssignmentResponse:
    return await service.create(data)


@router.post("/assignments")
async def create_daily_assignments_batch(
        data: list[schemas.DailyAssignmentCreate],
        service: AdminDailyAssignmentService = Depends()
) -> list[schemas.DailyAssignmentResponse]:
    return await service.create_daily_assignments_batch(data)


@router.patch("/")
async def edit_daily_assignment(
        daily_assignment_id: int,
        data: schemas.DailyAssignmentUpdate,
        service: AdminDailyAssignmentService = Depends()
) -> schemas.DailyAssignmentResponse:
    return await service.update(daily_assignment_id, data)


@router.delete("/")
async def delete_daily_assignment(
        daily_assignment_id: int,
        service: AdminDailyAssignmentService = Depends()
) -> schemas.SuccessResponse:
    return await service.delete(daily_assignment_id)


@router.delete("/group")
async def delete_daily_assignments_group(
        daily_assignment_id: int,
        service: AdminDailyAssignmentService = Depends()
) -> schemas.SuccessResponse:
    return await service.delete_daily_assignments_group(daily_assignment_id)
