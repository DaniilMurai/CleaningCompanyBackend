from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends, Query

import schemas
from api.admin.router.reports.service import AdminReportService

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/")
async def get_reports(
        params: Annotated[schemas.AdminReportFilterParams, Query()],
        service: AdminReportService = Depends()
) -> list[schemas.ReportResponse]:
    return await service.get_reports(params)


@router.patch("/")
async def update_report(
        report_id: int,
        data: schemas.UpdateReport,
        service: AdminReportService = Depends()
) -> schemas.ReportResponse:
    return await service.update(report_id, data)


@router.delete("/")
async def delete_report(
        report_id: int,
        service: AdminReportService = Depends()
) -> schemas.SuccessResponse:
    return await service.delete(report_id)
