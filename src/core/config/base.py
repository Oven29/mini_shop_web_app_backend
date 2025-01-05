import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


base_dir = Path(__file__).resolve().parents[3]


class ConfigError(ValueError):
    pass


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(base_dir, '.env'),
        env_file_encoding='utf-8',
        extra='ignore',
    )
