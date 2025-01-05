from abc import ABC, abstractmethod
import logging
from typing import Optional
from fastapi import Request

from core.config import settings
from core.config.payment_config import PaymentConfigBase
from schemas.payment import InvoiceSchema, InvoiceCreateSchema
from utils.other import to_snake_case


class BasePayment(ABC):
    """Base payment class"""
    origin: Optional[str] = None
    config: PaymentConfigBase

    def __init__(self, config: PaymentConfigBase) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = config

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
    async def cancel_invoice(self, pay_id: str) -> None:
        """
        Cancel invoice by payment id

        :param pay_id: payment id
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

    @property
    def name(self) -> str:
        """Payment method name"""
        return to_snake_case(self.__class__.__name__)
