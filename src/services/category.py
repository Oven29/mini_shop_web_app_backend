from typing import List, Optional

from exceptions.category import CategoryNotFoundError
from schemas.category import CategorySchema, CategoryCreateSchema, CategoryUpdateSchema
from schemas.product import ProductSchema
from .base import AbstractService


class CategoryService(AbstractService):
    async def get_all(self) -> List[CategorySchema]:
        async with self.uow:
            res = await self.uow.category.select()
            return [await e.to_schema() for e in res]

    async def check_exists(self, category_id: int) -> None:
        category = await self.uow.category.get(id=category_id)
        if category is None:
            raise CategoryNotFoundError(category_id)

    async def get_by_id(self, category_id: int) -> Optional[CategorySchema]:
        async with self.uow:
            await self.check_exists(category_id)
            res = await self.uow.category.get(id=category_id)
            return await res.to_schema()

    async def create(self, product: CategoryCreateSchema) -> CategorySchema:
        async with self.uow:
            res = await self.uow.category.create(**product.model_dump(exclude_unset=True))
            await self.uow.commit()
            return await res.to_schema()

    async def update(self, category_id: int, product: CategoryUpdateSchema) -> CategorySchema:
        async with self.uow:
            await self.check_exists(category_id)
            res = await self.uow.category.update(id=category_id, **product.model_dump(exclude_none=True))
            await self.uow.commit()
            return await res.to_schema()

    async def delete(self, category_id: int) -> CategorySchema:
        async with self.uow:
            await self.check_exists(category_id)
            res = await self.uow.category.delete(id=category_id)
            await self.uow.commit()
            return await res.to_schema()

    async def get_products(self, category_id: int) -> List[ProductSchema]:
        async with self.uow:
            await self.check_exists(category_id)
            res = await self.uow.product.select(category_id=category_id)
            return [await e.to_schema() for e in res]
