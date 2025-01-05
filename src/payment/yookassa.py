from typing import Any, Dict, Optional
import uuid
import aiohttp
from fastapi import Request

from enums.order import InvoiceStatus
from schemas.payment import InvoiceSchema, InvoiceCreateSchema
from .base import BasePayment


class YookassaPayment(BasePayment):
    """
    Yookassa payment

    Docs - https://yookassa.ru/developers/api?codeLang=python
    """
    async def _request(self, type: str, method: str, data: Dict[str, Any] = {}) -> Any:
        self.logger.debug(f'Requesting with {type=}, {method=}, {data=}')
        request_kwargs = {
            'url': f'{self.config.base_url}/{method}',
            'headers': {
                'Idempotence-Key': str(uuid.uuid4()),
                'Content-Type': 'application/json',
            },
        }
        if len(data):
            request_kwargs['json'] = data
        if self.config.oauth_token is not None:
            request_kwargs['headers']['Authorization'] = f'Bearer {self.config.oauth_token}'
        else:
            request_kwargs['auth']= aiohttp.BasicAuth(
                login=self.config.shop_id,
                password=self.config.secret_key,
            )

        async with aiohttp.ClientSession() as session:
            async with getattr(session, type)(**request_kwargs) as response:
                return await response.json()

    async def create_invoice(self, data: InvoiceCreateSchema) -> InvoiceSchema:
        # https://yookassa.ru/developers/api?codeLang=python#create_payment
        self.logger.debug(f'Creating invoice with {data=}')
        request_data = {
            'amount': {
                'value': str(data.amount),
                'currency': 'RUB'
            },
            'confirmation': {
                'type': 'redirect',
                'return_url': self.return_url,
            },
        }
        if data.description is not None:
            request_data['description'] = data.description

        response = await self._request(
            type='post',
            method='payments',
            data=request_data,
        )

        return InvoiceSchema(
            amount=data.amount,
            pay_id=response['id'],
            status=InvoiceStatus.WAIT,
            method=self.name,
            url=response['confirmation']['confirmation_url'],
            created_at=response['created_at'],
        )

    async def get_invoice(self, pay_id: str) -> InvoiceSchema:
        # https://yookassa.ru/developers/api?codeLang=python#get_payment
        self.logger.debug(f'Getting invoice {pay_id=}')
        response = await self._request(
            type='get',
            method=f'payments/{pay_id}',
        )

        return InvoiceSchema(
            amount=response['amount']['value'],
            pay_id=response['id'],
            status=InvoiceStatus.PAID if response['status'].lower() == 'succeeded' else InvoiceStatus.WAIT,
            method=self.name,
            url=response['confirmation']['confirmation_url'],
            created_at=response['created_at'],
        )

    async def cancel_invoice(self, pay_id: str) -> None:
        # https://yookassa.ru/developers/api?codeLang=bash#cancel_payment
        await self._request(
            type='post',
            method=f'payments/{pay_id}/cancel',
        )

    async def set_webhook(self) -> None:
        # https://yookassa.ru/developers/api?codeLang=bash#create_webhook
        if self.config.oauth_token is None:
            self.logger.warning('Webhook for Yookassa available only by OAuth token')
            self.polling_mode = True
            return

        self.logger.debug('Setting webhooks')
        await self._request(
            type='post',
            method='webhooks',
            data={
                'event': 'payment.succeeded',
                'url': self.webhook_url,
            },
        )

    async def handle_update(self, webhook: Request) -> Optional[InvoiceSchema]:
        # https://yookassa.ru/developers/api?codeLang=bash#webhook
        if webhook['event'] == 'payment.succeeded':
            return await self.get_invoice(webhook['id'])
