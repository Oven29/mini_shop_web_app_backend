from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from .media import MediaSchema


class CategorySchema(BaseModel):
    id: int
    name: str
    translit: str


class ProductSchema(BaseModel):
    id: int
    name: str
    translit: str
    description: Optional[str] = None
    price: int
    category: CategorySchema
    discount: Optional[int] = None
    discount_expire: Optional[datetime] = None
    amount: Optional[int] = None
    media: List[MediaSchema] = []


class ProductCreateSchema(ProductSchema):
    id: None = None
    translit: Optional[str] = None


class ProductUpdateSchema(ProductSchema):
    name: Optional[str] = None
    translit: Optional[str] = None
    price: Optional[str] = None
    category: None = None
    category_id: Optional[int] = None


class ProductDeleteSchema(BaseModel):
    id: int = None
