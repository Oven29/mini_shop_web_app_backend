from typing import List, Optional

from schemas.product import ProductSchema, ProductCreateSchema, ProductUpdateSchema
from .base import AbstractService


class ProductService(AbstractService):
    async def get_all(self) -> List[ProductSchema]:
        async with self.uow:
            res = await self.uow.product.select()
            return [e.to_schema() for e in res]

    async def get_by_id(self, product_id: int) -> Optional[ProductSchema]:
        async with self.uow:
            res = await self.uow.product.get(id=product_id)
            if res is None:
                return None
            return res.to_schema()

    async def create(self, product: ProductCreateSchema) -> ProductSchema:
        async with self.uow:
            res = await self.uow.product.create(**product.model_dump())
            await self.uow.commit()
            return res.to_schema()

    async def update(self, product_id: int, product: ProductUpdateSchema) -> ProductSchema:
        async with self.uow:
            res = await self.uow.product.update(id=product_id, **product.model_dump(exclude_none=True))
            if res is None:
                return
            await self.uow.commit()
            return res.to_schema()

    async def delete(self, product_id: int) -> ProductSchema:
        async with self.uow:
            res = await self.uow.product.delete(id=product_id)
            if res is None:
                return
            await self.uow.commit()
            return res.to_schema()
