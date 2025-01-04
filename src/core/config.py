import os
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel
import pydantic
from pydantic_settings import BaseSettings
from urllib.parse import quote


BASE_DIR: str = Path(__file__).resolve().parent.parent.parent
LOGS_DIR: str = os.path.join(BASE_DIR, 'logs')
UPLOADS_DIR: str = os.path.join(BASE_DIR, 'uploads')


class DbSettings(BaseModel):
    URL: str = 'sqlite+aiosqlite:///' + os.path.join(BASE_DIR, 'db.sqlite')
    DRIVER: str = 'postgresql+asyncpg'
    HOST: Optional[str] = None
    PORT: Optional[int] = None
    USER: Optional[str] = None
    PASSWORD: Optional[str] = None
    NAME: Optional[str] = None


class Settings(BaseSettings):
    DEBUG: bool = False
    RELOAD: bool = DEBUG
    LOGGING_LEVEL: str = 'DEBUG' if DEBUG else 'WARNING'

    HOST: str = '0.0.0.0'
    PORT: int = 8000

    DB: DbSettings = DbSettings()

    FRONTEND_URL: Optional[str] = None
    BOT_TOKEN: Optional[str] = None

    SECRET_KEY: str = '123456789abc'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    MAX_FILE_SIZE: int = 16 * 1024 * 1024  # 16 MB
    AVAILABLE_EXTENSIONS: List[str] = ['jpg', 'jpeg', 'png', 'mp4']
    BASE_URL: str = 'http://localhost:8000'

    @pydantic.computed_field()
    def DATABASE_URL(self) -> str:
        if self.DB.HOST and self.DB.PORT and self.DB.USER and self.DB.PASSWORD and self.DB.NAME:
            return (
                f'{self.DB.DRIVER}://{quote(self.DB.USER)}:{quote(self.DB.PASSWORD)}'
                f'@{self.DB.HOST}:{self.DB.PORT}/{self.DB.NAME}'
            )

        return self.DB.URL

    class Config:
        env_file = os.path.join(BASE_DIR, '.env')
        env_file_encoding = 'utf-8'


settings = Settings()
