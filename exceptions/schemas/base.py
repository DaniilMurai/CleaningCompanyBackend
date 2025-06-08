class SchemaValueError(ValueError):
    status_code: int | None = None
    message: str | None = None
    data: dict | None = None
