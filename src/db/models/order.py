from __future__ import annotations
from datetime import datetime
from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from enums.order import InvoiceStatus, OrderStatus
from ..base import Base
from .product import Product
from .user import User


class Invoice(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped[User] = relationship()

    order: Mapped[Order] = relationship(back_populates='invoice')

    amount: Mapped[float] = mapped_column(Float)
    status: Mapped[InvoiceStatus] = mapped_column(Enum(InvoiceStatus, native_enum=False))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    type: Mapped[str] = mapped_column(String(32))


class Order(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped[User] = relationship()

    invoice_id: Mapped[int] = mapped_column(ForeignKey('invoices.id'), nullable=False)
    invoice: Mapped[Invoice] = relationship(back_populates='order')

    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus, native_enum=False))
    amount: Mapped[int] = mapped_column(Integer)
    discount: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())


class OrderItem(Base):
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), nullable=False)
    order: Mapped[Order] = relationship(back_populates='items')

    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
    product: Mapped[Product] = relationship()

    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
