import logging
import os
from typing import List, Optional, Self
from pydantic import BaseModel, computed_field, model_validator

from .base import base_dir


class DirSettings(BaseModel):
    base: str = base_dir
    uploads: str = os.path.join(base_dir, 'uploads')

    @model_validator(mode='after')
    def validate(self) -> Self:
        if not os.path.exists(self.uploads):
            os.mkdir(self.uploads)

        return self


class RedisSettings(BaseModel):
    host: str = 'localhost'
    port: int = 6379

    @computed_field
    def url(self) -> str:
        return f'redis://{self.host}:{self.port}'


class FastapiSettings(BaseModel):
    host: str = '0.0.0.0'
    port: int = 8000
    reload: bool = False
    origins: List[str] = ['*']


class ProjectSettings(BaseModel):
    backend_url: Optional[str] = 'http://localhost:8000'
    frontend_url: Optional[str] = 'http://localhost:3000'


class FileSettings(BaseModel):
    max_size: int = 16 * 1024 * 1024  # Default 16 MB
    allowed_extensions: List[str] = ['jpg', 'jpeg', 'png', 'mp4']


class AuthSettings(BaseModel):
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 60 * 24  # Default 1 day


class LoggingSettings(BaseModel):
    level: str = 'WARNING'
    format: str = '[%(asctime)s | %(levelname)s | %(name)s]: %(message)s'
    datefmt: str = '%m.%d.%Y %H:%M:%S'

    @model_validator(mode='after')
    def validate(self) -> Self:
        logging.basicConfig(level=self.level, format=self.format, datefmt=self.datefmt)

        return self
