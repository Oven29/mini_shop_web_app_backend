from typing import List, Optional

from fastapi import Request

from enums.order import InvoiceStatus
from exceptions.common import BadRequestError, UnauthorizedError
from exceptions.payment import InvoiceForiddenError, InvoiceNotFoundError, PaymentMethodNotFoundError
from modules import payment
from schemas.payment import InvoiceCreateSchema, InvoiceSchema
from schemas.user import UserSchema
from .base import AbstractService


class PaymentService(AbstractService):
    async def get_methods(self) -> List[str]:
        return [m.name for m in payment.methods if m.config.enabled]

    def _get_method(self, name: str) -> payment.BasePayment:
        method = payment.name_to_method.get(name)
        if method is None or not method.config.enabled:
            raise PaymentMethodNotFoundError(name)
        return method

    async def create_invoice(self, data: InvoiceCreateSchema, user: UserSchema) -> InvoiceSchema:
        invoice = await self._get_method(data.method).create_invoice(data)
        async with self.uow:
            db_user = await self.uow.user.get(user_id=user.user_id)
            if db_user is None:
                raise UnauthorizedError
            await self.uow.invoice.create(
                pay_id=invoice.pay_id,
                amount=invoice.amount,
                status=invoice.status,
                method=invoice.method,
                created_at=invoice.created_at,
                user_id=db_user.id,
            )
            await self.uow.commit()
            return invoice

    async def get_invoice(self, pay_id: str, user: Optional[UserSchema] = None) -> InvoiceSchema:
        async with self.uow:
            invoice = await self.uow.invoice.get(pay_id=pay_id)
            if invoice is None:
                raise InvoiceNotFoundError(pay_id)

            if user is not None and invoice.user_id != user.id:
                raise InvoiceForiddenError(pay_id)

            return await invoice.to_schema()

    async def webhook(self, method: str, data: Request) -> None:
        res = await self._get_method(method).handle_update(data)
        if res is None:
            raise BadRequestError

        async with self.uow:
            await self.uow.invoice.update_status(
                pay_id=res.pay_id,
                status=res.status,
            )
            await self.uow.commit()
