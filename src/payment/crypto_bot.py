from typing import Optional
from aiocryptopay import AioCryptoPay, const
from fastapi import Request
from pydantic import BaseModel

from core.config import settings
from enums.order import InvoiceStatus
from schemas.payment import InvoiceSchema, InvoiceCreateSchema
from .base import BasePayment


class CryptoBotPayment(BasePayment):
    """
    CryptoBot payment

    Docs - https://help.crypt.bot/crypto-pay-api
    """
    def __init__(self, config: BaseModel) -> None:
        super().__init__(config)
        self.crypto = AioCryptoPay(
            token=self.config.token,
            network=self.config.network,
        )

    async def create_invoice(self, data: InvoiceCreateSchema) -> InvoiceSchema:
        # https://help.crypt.bot/crypto-pay-api#createInvoice
        invoice = await self.crypto.create_invoice(
            amount=data.amount,
            currency_type=const.CurrencyType.FIAT,
            fiat=const.Fiat.RUB,
            paid_btn_name='openBot',
            paid_btn_url=self.return_url,
            expires_in=settings.project.payment_time_life * 60,
            description=data.description,
        )

        return InvoiceSchema(
            pay_id=str(invoice.invoice_id),
            amount=invoice.amount,
            method=self.name,
            url=invoice.mini_app_invoice_url,
        )

    async def get_invoice(self, pay_id: str) -> Optional[InvoiceSchema]:
        # https://help.crypt.bot/crypto-pay-api#getInvoices
        invoices = await self.crypto.get_invoices(invoice_ids=[pay_id])
        if not len(invoices):
            return None

        return InvoiceSchema(
            pay_id=str(invoices[0].invoice_id),
            amount=invoices[0].amount,
            method=self.name,
            status=InvoiceStatus.PAID if invoices[0].status == const.InvoiceStatus.PAID else InvoiceStatus.WAIT,
            url=invoices[0].mini_app_invoice_url,
        )

    async def set_webhook(self) -> None:
        self.logger.warning(f'Webhook for {self.name} setting manually, '
            'more details - http://help.crypt.bot/crypto-pay-api#webhooks')

    async def handle_update(self, webhook: Request) -> Optional[InvoiceSchema]:
        # https://help.crypt.bot/crypto-pay-api#webhooks
        payload = webhook['payload']
        if payload.get('status') == const.InvoiceStatus.PAID:
            return InvoiceSchema(
                pay_id=str(payload['invoice_id']),
                amount=payload['amount'],
                method=self.name,
                status=InvoiceStatus.PAID,
                url=payload['url'],
            )
