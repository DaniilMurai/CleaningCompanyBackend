from starlette import status

from .base import SchemaValueError


class EndTimeMustBeAfterStartTime(SchemaValueError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    msg_template = "end_time ({end_time}) must be after start_time ({start_time})"


class IncorrectAdapterTypeValue(SchemaValueError):
    status_code = status.HTTP_400_BAD_REQUEST
    msg_template = "Incorrect Adapter type value: ({adapter_type})"
