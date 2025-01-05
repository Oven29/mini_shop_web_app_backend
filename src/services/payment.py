from enums.order import InvoiceStatus
from exceptions.payment import InvoiceNotFoundError
from schemas.payment import InvoiceSchema
from .base import AbstractService


class PaymentService(AbstractService):
    async def cancel(self, pay_id: str) -> InvoiceSchema:
        async with self.uow:
            invoice = self.uow.invoice.get(pay_id=pay_id)
            if invoice is None:
                raise InvoiceNotFoundError(pay_id)

            invoice = await self.uow.invoice.update(
                id=invoice.id,
                status=InvoiceStatus.CANCEL,
            )
            await self.uow.commit()
            return await invoice.to_schema()
