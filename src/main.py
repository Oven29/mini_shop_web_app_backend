import logging
import uvicorn
from fastapi import FastAPI

from api.v1 import v1_router
from core.config import settings
from exceptions.base import BaseException, exception_handler


logging.basicConfig(
    format='[%(asctime)s | %(levelname)s | %(name)s]: %(message)s',
    datefmt='%m.%d.%Y %H:%M:%S',
    level=settings.LOGGING_LEVEL,
)

app = FastAPI(
    title='Mini shop Tg web-app'
)

app.add_exception_handler(BaseException, exception_handler)
app.include_router(v1_router)


if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        reload=settings.RELOAD or settings.DEBUG,
        host=settings.HOST,
        port=settings.PORT,
    )
