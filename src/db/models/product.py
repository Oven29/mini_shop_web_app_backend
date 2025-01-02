from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from sqlalchemy import DateTime, ForeignKey, String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base
from .media import Media


class Category(Base):
    __tablename__ = 'categories'

    name: Mapped[str] = mapped_column(String(256), nullable=False)
    translit: Mapped[str] = mapped_column(String(256), nullable=False)
    products: Mapped[List[Product]] = relationship(back_populates='category', cascade='all, delete-orphan')


class Product(Base):
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    translit: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    discount: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    discount_expire: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    amount: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False)
    category: Mapped[Category] = relationship(back_populates='products')

    media: Mapped[List[ProductImage]] = relationship(back_populates='product', cascade='all, delete-orphan')


class ProductImage(Base):
    media_id: Mapped[int] = mapped_column(ForeignKey('media.id'))
    media: Mapped[Media] = relationship()
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    product: Mapped[Product] = relationship(back_populates='media')
