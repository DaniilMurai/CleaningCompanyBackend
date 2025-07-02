from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.responses import FileResponse

import schemas
from api.admin.router.export_reports.service import AdminExportReportService
from api.depends.lang import get_lang

router = APIRouter(prefix="/export-reports", tags=['export-reports'])


@router.post("/")
async def create_export_reports(
        params: schemas.ReportExportParams,
        lang: Annotated[str, Query()],
        service: AdminExportReportService = Depends()
) -> int:
    print(lang)
    params.lang = get_lang(lang)
    print(params.lang)
    return await service.export_reports(params)


@router.get("/{export_id}/download")
async def download_export(
        export_id: int,
        service: AdminExportReportService = Depends()
) -> FileResponse:
    return await service.download_report(export_id)


@router.get("/")
async def get_export_reports(
        params: Annotated[schemas.AdminGetListParams, Query()],
        service: AdminExportReportService = Depends()
) -> list[schemas.ReportExportResponse]:
    return await service.get_export_reports(params)
