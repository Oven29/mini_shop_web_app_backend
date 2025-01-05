from datetime import datetime
from typing import Any, Optional

from enums.order import InvoiceStatus
from schemas.payment import InvoiceSchema
from ..models.order import Order, Invoice
from .base import SQLAlchemyRepository


class InvoiceRepository(SQLAlchemyRepository[Invoice]):
    model = Invoice

    async def update_status(self, pay_id: str, status: InvoiceStatus) -> Optional[InvoiceSchema]:
        """
        Update invoice status

        :param pay_id: payment id
        :param status: invoice status
        :return: updated invoice
        """
        invoice = self.get(pay_id=pay_id)
        if invoice is None:
            return None

        invoice = await self.update(
            id=invoice.id,
            status=status,
        )
        return await invoice.to_schema()

    async def cancel(self, pay_id: str) -> Optional[InvoiceSchema]:
        """
        Update invoice status to cancel

        :param pay_id: payment id
        :return: updated invoice
        """
        return await self.update_status(pay_id=pay_id, status=InvoiceStatus.CANCEL)


class OrderRepository(SQLAlchemyRepository[Order]):
    model = Invoice

    async def update(self, id: int, **values: Any) -> Order:
        if 'updated_at' not in values:
            values['updated_at'] = datetime.now()
        return await super().update(id=id, **values)
