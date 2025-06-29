from fastapi import Header

from config import settings
from utils.api import parse_accept_language


def get_lang(
        header_lang: str | None = Header(None, alias="Accept-Language"),
):
    if not header_lang:
        return settings.DEFAULT_LANG
    return parse_accept_language(header_lang)
