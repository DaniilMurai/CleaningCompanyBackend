from fastapi import APIRouter
from fastapi.params import Depends, Query

import schemas
from api.client.router.reports.service import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])

MAX_IDS = 100


@router.get("/")
async def get_reports_by_assignment_ids(
        assignment_ids: list[int] = Query(..., alias="id", max_length=MAX_IDS),
        service: ReportService = Depends()
) -> list[schemas.ReportResponse]:
    return await service.get_reports_by_assignment_ids(assignment_ids)


@router.post("/")
async def create_report(
        data: schemas.CreateReport,
        service: ReportService = Depends()
) -> schemas.ReportResponse:
    return await service.create_report(data)

# @router.patch("/")
# async def update_report(
#         report_id: int,
#         data: schemas.UpdateReport,
#         service: ReportService = Depends()
# ) -> schemas.ReportResponse:
#     return await service.update_report(report_id, data)
