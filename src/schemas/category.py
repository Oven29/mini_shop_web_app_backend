from typing import Optional
from pydantic import BaseModel


class CategorySchema(BaseModel):
    id: int
    name: str
    translit: str


class CategoryCreateSchema(BaseModel):
    name: str
    translit: Optional[str] = None


class CategoryUpdateSchema(BaseModel):
    name: Optional[str] = None
    translit: Optional[str] = None
