import logging
from typing import Optional, Self
from aiocryptopay import Networks
from pydantic import SecretStr, model_validator
from pydantic_settings import SettingsConfigDict

from .base import ConfigBase


logger = logging.getLogger(__name__)


class PaymentConfigBase(ConfigBase):
    enabled: bool = True


class CryptoBotConfig(PaymentConfigBase):
    model_config = SettingsConfigDict(env_prefix='CRYPTO_BOT_')

    token: Optional[SecretStr] = None
    network: str = Networks.MAIN_NET

    @model_validator(mode='after')
    def validate(self) -> Self:
        if self.token is None and self.enabled:
            logger.warning('CryptoBot payment disabled, because no token provided')
            self.enabled = False

        return self


class YookassaConfig(PaymentConfigBase):
    model_config = SettingsConfigDict(env_prefix='YOOKASSA_')

    shop_id: Optional[int] = None
    secret_key: Optional[SecretStr] = None
    oauth_token: Optional[SecretStr] = None
    base_url: str = 'https://api.yookassa.ru/v3'

    @model_validator(mode='after')
    def validate(self) -> Self:
        if self.shop_id is None and self.secret_key is None and self.oauth_token is None and self.enabled:
            logger.warning('Yookassa payment disabled, because no credentials provided')
            self.enabled = False

        return self
