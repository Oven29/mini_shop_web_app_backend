import os
from typing import Optional, Self
from urllib.parse import quote, urlparse
import requests
from pydantic import SecretStr, computed_field, model_validator
from pydantic_settings import SettingsConfigDict

from .base import ConfigBase, ConfigError, base_dir


class DatabaseConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix='DB_')

    url: SecretStr = SecretStr('sqlite+aiosqlite:///' + os.path.join(base_dir, 'db.sqlite'))
    driver: str = 'postgresql+asyncpg'
    host: Optional[str] = None
    port: Optional[int] = None
    user: Optional[str] = None
    password: Optional[SecretStr] = None
    name: Optional[str] = None

    @model_validator(mode='after')
    def validate(self) -> Self:
        if [self.driver, self.host, self.port, self.user, self.password, self.name].count(None) == 0:
            self.url = SecretStr(
                f'{self.driver}://{quote(self.user)}:{quote(self.password.get_secret_value())}'
                f'@{self.host}:{self.port}/{self.name}'
            )

        elif self.url:
            parsed_url = urlparse(self.url.get_secret_value())
            self.driver = parsed_url.scheme
            self.host = parsed_url.hostname
            self.port = parsed_url.port
            self.user = parsed_url.username
            self.password = SecretStr(parsed_url.password)
            self.name = parsed_url.path

        else:
            raise ConfigError('DB was not configured')

        return self


class AppConfig(ConfigBase):
    secret_key: SecretStr
    debug: bool = False


class TelegramConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix='TG_')

    bot_token: SecretStr
    bot_username: Optional[str] = None

    @computed_field()
    def bot_url(self) -> str:
        return f'https://t.me/{self.bot_username}'

    @model_validator(mode='after')
    def validate(self) -> Self:
        if self.bot_username is None:
            response = requests.get(f'https://api.telegram.org/bot{self.bot_token.get_secret_value()}/getMe')
            response = response.json()
            if not response['ok']:
                raise ConfigError('Wrong bot token configured')
            self.bot_username = response['result']['username']

        return self
