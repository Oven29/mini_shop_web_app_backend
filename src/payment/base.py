from abc import ABC, abstractmethod
import logging
from typing import Any, Optional
from fastapi import Request
from pydantic import BaseModel

from core.config import settings
from schemas.payment import InvoiceSchema, InvoiceCreateSchema
from utils.other import to_snake_case


class BasePayment(ABC):
    """Base payment class"""
    name: str = None
    origin: Optional[str] = None

    def __init__(self, config: BaseModel) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = config

    def __init_subclass__(cls, **kwargs: Any) -> None:
        if getattr(cls, 'name', None) is None:
            cls.name = to_snake_case(cls.__name__)

        return super().__init_subclass__(**kwargs)

    @abstractmethod
    async def create_invoice(self, data: InvoiceCreateSchema) -> InvoiceSchema:
        """
        Create invoice

        :param data: data for create invoice
        :return: created invoice
        """
        raise NotImplementedError

    @abstractmethod
    async def get_invoice(self, pay_id: str) -> Optional[InvoiceSchema]:
        """
        Get invoice by payment id

        :param pay_id: payment id
        :return: invoice or None
        """
        raise NotImplementedError

    @abstractmethod
    async def set_webhook(self) -> None:
        """
        Set webhook
        """
        raise NotImplementedError

    @abstractmethod
    async def handle_update(self, webhook: Request) -> Optional[InvoiceSchema]:
        """
        Handle update webhook
        
        :param webhook: webhook data
        :return: invoice or None
        """
        raise NotImplementedError

    @property
    def webhook_url(self) -> str:
        """Webhook url"""
        return f'{settings.project.backend_url}/v1/payment/webhook/{self.name}'

    @property
    def return_url(self) -> str:
        """Return url"""
        return settings.tg.bot_url
