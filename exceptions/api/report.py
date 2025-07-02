from starlette import status

from .base import APIException


class ReportExportStatusFailed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, data: dict | None = None):
        self.data = data


class ReportExportIsNotCompletedYet(APIException):
    status_code = status.HTTP_425_TOO_EARLY

    def __init__(self, data: dict | None = None):
        self.data = data


class ErrorDuringReportCreate(APIException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, data: dict | None = None):
        self.data = data
