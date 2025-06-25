from fastapi import APIRouter, Depends

import schemas
from api.client.router.assignments.service import AssignmentService

router = APIRouter(prefix="/assignments", tags=["assignments"])


@router.get("/daily-assignments")
async def get_daily_assignments(
        service: AssignmentService = Depends()
) -> list[schemas.DailyAssignmentForUserResponse]:
    return await service.get_daily_assignments()


@router.get("/daily-assignment")
async def get_daily_assignment_by_id(
        assignment_id: int,
        service: AssignmentService = Depends()
) -> schemas.DailyAssignmentForUserResponse:
    return await service.get_daily_assignment_by_id(assignment_id)


@router.get("/daily-assignments-and-reports")
async def get_daily_assignments_and_reports(
        service: AssignmentService = Depends()
) -> list[schemas.AssignmentReportResponse]:
    return await service.get_daily_assignments_and_reports()


@router.get("/{report_id}")
async def get_daily_assignment_and_report_by_report_id(
        report_id: int,
        service: AssignmentService = Depends()
):
    return await service.get_daily_assignment_and_report_by_report_id(report_id)


@router.patch("/")
async def update_daily_assignment(
        assignment_id: int,
        data: schemas.DailyAssignmentForUserUpdate,
        service: AssignmentService = Depends()
) -> schemas.DailyAssignmentForUserResponse:
    return await service.update_daily_assignment(assignment_id, data)


@router.patch("/daily-assignment")
async def update_daily_assignment_status(
        assignment_id: int,
        status: schemas.AssignmentStatus,
        service: AssignmentService = Depends()
) -> schemas.DailyAssignmentForUserResponse:
    return await service.update_daily_assignment_status(assignment_id, status)
