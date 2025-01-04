from typing import List, Optional
from pydantic import BaseModel

from .product import ProductSchema


class CategorySchema(BaseModel):
    id: int
    name: str
    translit: str
    products: List[ProductSchema] = []


class CategoryCreateSchema(BaseModel):
    name: str
    translit: Optional[str] = None


class CategoryUpdateSchema(BaseModel):
    name: Optional[str] = None
    translit: Optional[str] = None
