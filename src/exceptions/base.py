from typing import Any, Dict, Type

from fastapi.responses import JSONResponse

from schemas.common import ErrorResponse


class BaseApiError(Exception):
    model: ErrorResponse
    status_code: int
    error_schema: Dict[str, Type[ErrorResponse]]

    class Model(ErrorResponse):
        pass

    def __init__(self, **kwargs: Any) -> None:
        self.model = self.Model(**kwargs)
        super().__init__(self.model.detail)

    def __init_subclass__(cls) -> None:
        cls.status_code = cls.Model.model_fields['status_code'].default
        cls.error_schema = {'model': cls.Model}

        return super().__init_subclass__()


async def exception_handler(request: Any, exc: BaseApiError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.model.model_dump(),
    )
