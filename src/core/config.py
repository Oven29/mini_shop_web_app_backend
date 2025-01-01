import os
from pathlib import Path
import sys
from typing import Optional
from pydantic_settings import BaseSettings
from urllib.parse import quote


BASE_DIR: str = Path(__file__).resolve().parent.parent
LOGS_DIR: str = os.path.join(BASE_DIR, 'logs')
UPLOADS_DIR: str = os.path.join(BASE_DIR, 'uploads')


class Settings(BaseSettings):
    DEBUG: bool = False

    HOST: str = '0.0.0.0'
    PORT: int = 8000

    DB_URL: Optional[str] = None

    DB_DRIVER: str = 'postgresql+asyncpg'
    DB_HOST: Optional[str] = None
    DB_PORT: Optional[int] = None
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_NAME: Optional[str] = None

    FRONTEND_URL: str
    BOT_TOKEN: str

    SECRET_KEY: str = '123456789abc'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    def get_db_url(self) -> str:
        if self.DB_URL:
            return self.DB_URL

        assert self.DB_HOST and self.DB_PORT and self.DB_USER and self.DB_PASSWORD and self.DB_NAME

        return (
            f'{self.DB_DRIVER}://{quote(self.DB_USER)}:{quote(self.DB_PASSWORD)}'
            f'@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        )

    class Config:
        env_file = os.path.join(BASE_DIR, '.env')


if len(sys.argv) == 1:    
    settings = Settings()

elif sys.argv[1] == 'dev':
    settings = Settings(
        _env_file=os.path.join(BASE_DIR, '.env.dev'),
        DEBUG=True,
        DB_URL='sqlite+aiosqlite:///' + os.path.join(BASE_DIR, 'db.sqlite'),
    )

else:
    raise AttributeError('Project runned with unknown cmd argument')
