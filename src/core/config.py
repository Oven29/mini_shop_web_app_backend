from __future__ import annotations
import logging
import os
from pathlib import Path
from typing import Any, List, Optional, Self, Tuple
from pydantic import BaseModel, Field, model_validator, computed_field
from pydantic.types import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict, TomlConfigSettingsSource
from urllib.parse import quote, urlparse


_base_dir = Path(__file__).resolve().parent.parent.parent


class ConfigError(Exception):
    pass


class DirSettings(BaseModel):
    base: str = _base_dir
    uploads: str = os.path.join(_base_dir, 'uploads')

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


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(_base_dir, '.env'),
        env_file_encoding='utf-8',
        extra='ignore',
    )


class AppConfig(ConfigBase):
    secret_key: SecretStr
    debug: bool = False


class TelegramConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix='TG_')

    bot_token: SecretStr
    bot_username: str

    @computed_field
    def bot_url(self) -> str:
        return f'https://t.me/{self.bot_username}'


class DatabaseConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix='DB_')

    url: SecretStr = SecretStr('sqlite+aiosqlite:///' + os.path.join(_base_dir, 'db.sqlite'))
    driver: str = 'postgresql+asyncpg'
    host: Optional[str] = None
    port: Optional[int] = None
    user: Optional[str] = None
    password: Optional[SecretStr] = None
    name: Optional[str] = None

    @model_validator(mode='after')
    def validate(self) -> Self:
        if self.host and self.port and self.user and self.password and self.name:
            self.url = (
                f'{self.driver}://{quote(self.user)}:{quote(self.password.get_secret_value())}'
                f'@{self.host}:{self.port}/{self.name}'
            )

        elif self.url:
            parsed_url = urlparse(self.url.get_secret_value())
            self.driver = parsed_url.scheme
            self.host = parsed_url.hostname
            self.port = parsed_url.port
            self.user = parsed_url.username
            self.password = parsed_url.password
            self.name = parsed_url.path

        else:
            raise ConfigError('DB was not configured')

        return self


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')

    db: DatabaseConfig = Field(default_factory=DatabaseConfig)
    tg: TelegramConfig = Field(default_factory=TelegramConfig)
    app: AppConfig = Field(default_factory=AppConfig)

    dir: DirSettings = Field(default_factory=DirSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    fastapi: FastapiSettings = Field(default_factory=FastapiSettings)
    project: ProjectSettings = Field(default_factory=ProjectSettings)
    file: FileSettings = Field(default_factory=FileSettings)
    auth: AuthSettings = Field(default_factory=AuthSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)

    @classmethod
    def load(cls) -> Settings:
        return cls()

    @classmethod
    def settings_customise_sources(cls, settings_cls: Any, **kwargs: Any) -> Tuple[Any, ...]:
        return (TomlConfigSettingsSource(settings_cls, os.path.join(_base_dir, 'config.toml')),)


try:
    settings = Settings.load()
except Exception as e:
    raise ConfigError(str(e))
