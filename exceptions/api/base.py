import re


class APIException(Exception):
    status_code: int
    message: str | None = None
    data: dict | None = None

    def __init_subclass__(cls):
        if cls.message is None:
            cls.message = paschal_case_to_human_case(cls.__name__)


def paschal_case_to_human_case(string: str) -> str:
    return " ".join(
        [word.lower() for word in
         re.findall(r"[A-Z](?:[A-Z](?![a-z0-9]))*[a-z0-9]*", string)]
    )
