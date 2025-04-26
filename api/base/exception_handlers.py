import http
import sys
import traceback
from functools import wraps
from typing import Awaitable, Callable

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.utils import is_body_allowed_for_status_code
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from config import settings
from exceptions import APIException
from loggers import JSONLogger
from utils.api import parse_accept_language

logger = JSONLogger()


def api_error_handler(func) -> Callable[[Request, Exception], Awaitable[Response]]:
    @wraps(func)
    async def wrapper(request: Request, error: Exception):
        request.state.exception_info = {
            "message": f"{error.__class__.__name__}: {str(error)}",
            "info": "".join(traceback.format_exception(*sys.exc_info())),
        }
        return await func(request, error)

    return wrapper


@api_error_handler
async def api_exception_handler(
        request: Request, error: APIException
):
    lang = parse_accept_language(
        request.headers.get("Accept-Language", settings.DEFAULT_LANG)
    )

    status_code = error.status_code
    detail_text = error.message
    detail_data = error.data

    logger.error(
        error, {
            "detail_text": detail_text,
            "detail_data": detail_data,
            "lang": lang,
        }
    )

    headers = getattr(error, "headers", None)
    if not is_body_allowed_for_status_code(status_code):
        return Response(status_code=status_code, headers=headers)

    content = {
        "detail": detail_text or ""
    }
    if detail_data:
        content["detail_data"] = detail_data

    return JSONResponse(
        content, status_code=status_code, headers=headers
    )


@api_error_handler
async def http_exception_handler(_: Request, error: HTTPException):
    logger.error(error)

    headers = getattr(error, "headers", None)
    if not is_body_allowed_for_status_code(error.status_code):
        return Response(status_code=error.status_code, headers=headers)

    return JSONResponse(
        {"detail": error.detail}, status_code=error.status_code, headers=headers
    )


@api_error_handler
async def request_validation_error(_: Request, error: RequestValidationError):
    logger.error(error)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": repr(error)}
    )


@api_error_handler
async def unhandled_exception_handler(_: Request, error: Exception):
    logger.error(error)

    detail = http.HTTPStatus(500).phrase
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": detail},
    )


def register_general_exception_handlers(app: FastAPI):
    app.add_exception_handler(APIException, api_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, request_validation_error)
    app.add_exception_handler(Exception, unhandled_exception_handler)
