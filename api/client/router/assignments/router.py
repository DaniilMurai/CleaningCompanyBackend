from fastapi import APIRouter, Depends

import schemas
from api.client.router.assignments.service import AssignmentService

router = APIRouter(prefix="/assignments", tags=["assignments"])


@router.get("/daily-assignment")
async def get_daily_assignment(
        service: AssignmentService = Depends()
) -> list[schemas.DailyAssignmentForUserResponse]:
    return await service.get_daily_assignment()
