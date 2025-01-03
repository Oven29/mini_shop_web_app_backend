from typing import List

from schemas.product import ProductSchema, ProductCreateSchema, ProductUpdateSchema
from .base import AbstractService


class ProductService(AbstractService):
    async def get_all(self) -> List[ProductSchema]:
        async with self.uow:
            return await self.uow.product.select()

    async def get_by_id(self, product_id: int) -> ProductSchema:
        async with self.uow:
            return await self.uow.product.get(id=product_id)

    async def create(self, product: ProductCreateSchema) -> ProductSchema:
        async with self.uow:
            return (await self.uow.product.create(**product.model_dump())).to_schema()

    async def update(self, product: ProductUpdateSchema) -> ProductSchema:
        async with self.uow:
            return (await self.uow.product.update(**product.model_dump(exclude_none=True))).to_schema()

    async def delete(self, product_id: int) -> ProductSchema:
        async with self.uow:
            return (await self.uow.product.delete(id=product_id)).to_schema()
