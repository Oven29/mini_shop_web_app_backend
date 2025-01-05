from __future__ import annotations
import os
from typing import Any, Tuple
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict, TomlConfigSettingsSource

from .base import ConfigError, base_dir
from .common_config import DatabaseConfig, TelegramConfig, AppConfig
from .payment_config import CryptoBotConfig, YookassaConfig
from .settings import (
    DirSettings,
    RedisSettings,
    FastapiSettings,
    ProjectSettings,
    FileSettings,
    AuthSettings,
    LoggingSettings,
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')

    db: DatabaseConfig = Field(default_factory=DatabaseConfig)
    tg: TelegramConfig = Field(default_factory=TelegramConfig)
    app: AppConfig = Field(default_factory=AppConfig)

    yookassa: YookassaConfig = Field(default_factory=YookassaConfig)
    cryptobot: CryptoBotConfig = Field(default_factory=CryptoBotConfig)

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
        return (TomlConfigSettingsSource(settings_cls, os.path.join(base_dir, 'config.toml')),)


try:
    settings = Settings.load()
except Exception as e:
    raise ConfigError(str(e))
