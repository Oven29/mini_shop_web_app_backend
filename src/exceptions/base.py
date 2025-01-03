from typing import Any

from fastapi.responses import JSONResponse


class BaseException(Exception):
    message: str
    status_code: int


async def exception_handler(request: Any, exc: BaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail': f'{exc.status_code} - {exc.message}'},
    )
