from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

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


@router.get("/{export_id}/download")
async def download_export(
        export_id: int,
        service: AdminExportReportService = Depends()
) -> FileResponse:
    return await service.download_report(export_id)


# Не работает
@router.get("/")
async def get_export_reports(
        service: AdminExportReportService = Depends()
):
    return await service.get_list()
