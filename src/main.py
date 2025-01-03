import uvicorn
from fastapi import FastAPI

from api.v1 import v1_router
from core.config import settings


app = FastAPI(
    title='Mini shop Tg web-app'
)


app.include_router(v1_router)


if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        reload=settings.DEBUG,
        host=settings.HOST,
        port=settings.PORT,
    )
