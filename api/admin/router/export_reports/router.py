from fastapi import APIRouter, Depends

import schemas
from api.admin.router.export_reports.service import AdminExportReportService

router = APIRouter(prefix="/export-reports", tags=['export-reports'])


@router.post("/")
async def create_export_reports(
        params: schemas.ReportExportParams,
        service: AdminExportReportService = Depends()
) -> int:
    return await service.export_reports(params)


@router.get("/")
async def get_export_reports(
        service: AdminExportReportService = Depends()
):
    return await service.get_list()
