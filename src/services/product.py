from typing import List, Optional

from exceptions.product import ProductNotFoundError
from schemas.product import ProductSchema, ProductCreateSchema, ProductUpdateSchema
from .base import AbstractService


class ProductService(AbstractService):
    async def get_all(self) -> List[ProductSchema]:
        async with self.uow:
            res = await self.uow.product.select()
            return [await e.to_schema() for e in res]

    async def check_exists(self, product_id: int) -> None:
        product = await self.uow.product.get(id=product_id)
        if product is None:
            raise ProductNotFoundError(product_id)

    async def get_by_id(self, product_id: int) -> Optional[ProductSchema]:
        async with self.uow:
            await self.check_exists(product_id)
            res = await self.uow.product.get(id=product_id)
            return await res.to_schema()

    async def create(self, product: ProductCreateSchema) -> ProductSchema:
        async with self.uow:
            res = await self.uow.product.create(**product.model_dump(exclude_unset=True))
            await self.uow.commit()
            return await res.to_schema()

    async def update(self, product_id: int, product: ProductUpdateSchema) -> ProductSchema:
        async with self.uow:
            await self.check_exists(product_id)
            res = await self.uow.product.update(id=product_id, **product.model_dump(exclude_none=True))
            await self.uow.commit()
            return await res.to_schema()

    async def delete(self, product_id: int) -> ProductSchema:
        async with self.uow:
            await self.check_exists(product_id)
            res = await self.uow.product.delete(id=product_id)
            await self.uow.commit()
            return await res.to_schema()

    async def search(self, query: str) -> List[ProductSchema]:
        async with self.uow:
            res = await self.uow.product.search(query)
            return [await e.to_schema() for e in res]
