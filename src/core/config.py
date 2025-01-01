import os
from pathlib import Path
import sys
from pydantic_settings import BaseSettings
from pydantic import computed_field
from urllib.parse import quote


BASE_DIR: str = Path(__file__).resolve().parent.parent
LOGS_DIR: str = os.path.join(BASE_DIR, 'logs')
UPLOADS_DIR: str = os.path.join(BASE_DIR, 'uploads')


class Base(BaseSettings):
    class Config:
        env_file = os.path.join(BASE_DIR, '.env')


class DBSettings(Base):
    DB_DRIVER: str = 'postgresql+asyncpg'
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @computed_field()
    def DB_URL(self) -> str:
        return (
            f'{self.DB_DRIVER}://{quote(self.DB_USER)}:{quote(self.DB_PASSWORD)}'
            f'@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        )


class Settings(Base):
    DEBUG: bool = False
    HOST: str = '0.0.0.0'
    PORT: int = 8000

    DB_URL: str

    FRONTEND_URL: str
    BOT_TOKEN: str
    SECRET_KEY: str = '123456789abc'


db_settings = None

if len(sys.argv) > 1 and sys.argv[1] == 'dev':
    settings = Settings(
        _env_file=os.path.join(BASE_DIR, '.env.dev'),
        DEBUG=True,
        DB_URL='sqlite+aiosqlite:///' + os.path.join(BASE_DIR, 'db.sqlite'),
    )
else:
    db_settings = DBSettings()
    settings = Settings(
        DB_URL=db_settings.DB_URL,
    )
