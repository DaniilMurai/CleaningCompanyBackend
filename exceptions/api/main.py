from starlette import status

from .base import APIException


class TestError(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "Test error"

    def __init__(self, data: dict | None = None):
        self.data = data
