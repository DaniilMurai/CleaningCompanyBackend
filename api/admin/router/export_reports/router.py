from fastapi import APIRouter, Depends

import schemas
from api.admin.router.export_reports.service import AdminExportReportService
from api.depends.lang import get_lang

router = APIRouter(prefix="/export-reports", tags=['export-reports'])


@router.post("/")
async def create_export_reports(
        params: schemas.ReportExportParams,
        lang: str = Depends(get_lang),
        service: AdminExportReportService = Depends()
) -> int:
    params.lang = lang
    return await service.export_reports(params)


@router.get("/")
async def get_export_reports(
        service: AdminExportReportService = Depends()
):
    return await service.get_list()
