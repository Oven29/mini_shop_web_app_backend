from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from .media import MediaSchema


class ProductSchema(BaseModel):
    id: int
    name: str
    translit: str
    description: Optional[str] = None
    price: int
    category_id: int
    discount: Optional[int] = None
    discount_expire: Optional[datetime] = None
    amount: Optional[int] = None
    media: List[MediaSchema] = []


class ProductCreateSchema(BaseModel):
    name: str
    translit: Optional[str] = None
    description: Optional[str] = None
    price: int
    category_id: int
    discount: Optional[int] = None
    discount_expire: Optional[datetime] = None
    amount: Optional[int] = None
    media: List[int] = []


class ProductUpdateSchema(BaseModel):
    name: Optional[str] = None
    translit: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    category_id: Optional[int] = None
    discount: Optional[int] = None
    discount_expire: Optional[datetime] = None
    amount: Optional[int] = None
    media: Optional[List[int]] = None
