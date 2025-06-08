from fastapi import APIRouter
from fastapi.params import Depends

import schemas
from api.client.router.reports.service import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/")
async def get_reports(
        assignment_ids: list[int],
        service: ReportService = Depends()
):
    return await service.get_reports(assignment_ids)


@router.post("/")
async def create_report(
        data: schemas.CreateReport,
        service: ReportService = Depends()
) -> schemas.ReportResponse:
    return await service.create_report(data)


@router.patch("/")
async def update_report(
        report_id: int,
        data: schemas.UpdateReport,
        service: ReportService = Depends()
) -> schemas.ReportResponse:
    return await service.update_report(report_id, data)
