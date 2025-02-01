from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from sqlalchemy import DateTime, ForeignKey, String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from schemas.category import CategorySchema
from schemas.product import ProductSchema
from schemas.media import MediaSchema
from ..base import Base
from .media import Media


class Category(Base):
    __tablename__ = 'categories'
    __schema__ = CategorySchema

    name: Mapped[str] = mapped_column(String(256), nullable=False)
    translit: Mapped[str] = mapped_column(String(256), nullable=False)

    parent_category_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('categories.id', ondelete='CASCADE'), nullable=True)

    products: Mapped[List[Product]] = relationship(back_populates='category', cascade='all, delete-orphan')

    parent_category: Mapped[Optional[Category]] = relationship(back_populates='subcategories', remote_side='Category.id')
    subcategories: Mapped[List[Category]] = relationship(back_populates='parent_category', cascade='all, delete-orphan')

    async def to_schema(
        self,
        include_subcategories: bool = False,
        include_parent_category: bool = False,
    ) -> CategorySchema:
        if include_subcategories:
            subcategories = await self.awaitable_attrs.subcategories
            subcategories = [await subcategory.to_schema() for subcategory in subcategories]
        else:
            subcategories = []
    
        parent_category = None
        if include_parent_category:
            parent_category = await self.awaitable_attrs.parent_category
            if not parent_category is None:
                parent_category = await parent_category.to_schema()

        return CategorySchema(
            id=self.id,
            name=self.name,
            translit=self.translit,
            products=await self.awaitable_attrs.products,
            parent_category_id=self.parent_category_id,
            subcategories=subcategories,
            parent=parent_category,
        )


class Product(Base):
    __schema__ = ProductSchema

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

    async def to_schema(self) -> MediaSchema:
        return await self.media.to_schema()
