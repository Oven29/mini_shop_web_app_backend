from .base import SQLAlchemyRepository
from ..models.order import Order, Invoice


class InvoiceRepository(SQLAlchemyRepository[Invoice]):
    pass


class OrderRepository(SQLAlchemyRepository[Order]):
    pass
