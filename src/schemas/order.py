from datetime import datetime
from typing import List
from pydantic import BaseModel

from enums.order import OrderStatus
from .product import ProductSchema
from .user import UserSchema


class OrderSchema(BaseModel):
    id: int
    amount: int
    discount: int
    status: OrderStatus
    user: UserSchema
    items: List[ProductSchema]
    created_at: datetime
