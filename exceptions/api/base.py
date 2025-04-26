class APIException(Exception):
    status_code: int
    message: str | None = None
    data: dict | None = None
