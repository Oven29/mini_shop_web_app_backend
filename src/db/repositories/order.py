from .base import SQLAlchemyRepository
from ..models.order import Order, Invoice


class InvoiceRepository(SQLAlchemyRepository[Invoice]):
    model = Invoice


class OrderRepository(SQLAlchemyRepository[Order]):
    model = Invoice
