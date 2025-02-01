from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel

from .product import ProductSchema


class CategorySchema(BaseModel):
    id: int
    name: str
    translit: str
    products: List[ProductSchema] = []
    parent_category_id: Optional[int] = None
    subcategories: List[CategorySchema] = []
    parent: Optional[CategorySchema] = None


class CategoryCreateSchema(BaseModel):
    name: str
    translit: Optional[str] = None
    parent_category_id: Optional[int] = None


class CategoryUpdateSchema(BaseModel):
    name: Optional[str] = None
    translit: Optional[str] = None
    parent_category_id: Optional[int] = None
