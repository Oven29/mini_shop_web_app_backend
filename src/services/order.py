from typing import List, Optional

from schemas.order import OrderSchema
from .base import AbstractService


class CategoryService(AbstractService):
    async def reserve(self) -> OrderSchema:
        async with self.uow:
            pass
