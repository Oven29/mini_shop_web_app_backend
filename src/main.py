import logging
import uvicorn
from fastapi import FastAPI

from api.v1 import v1_router
from core.config import settings
from exceptions.base import BaseApiError, exception_handler


app = FastAPI(
    title='Mini shop Tg web-app',
    debug=settings.app.debug,
)

app.add_exception_handler(BaseApiError, exception_handler)
app.include_router(v1_router)


if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        reload=settings.fastapi.reload,
        host=settings.fastapi.host,
        port=settings.fastapi.port,
    )
