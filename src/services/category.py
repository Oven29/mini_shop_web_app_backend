from typing import List, Optional

from exceptions.category import CategoryNotFoundError
from schemas.category import CategorySchema, CategoryCreateSchema, CategoryUpdateSchema
from .base import AbstractService


class CategoryService(AbstractService):
    async def get_all(self) -> List[CategorySchema]:
        async with self.uow:
            res = await self.uow.category.select()
            return [e.to_schema() for e in res]

    def check_result(self, id: int, res: CategorySchema | None) -> None:
        if res is None:
            raise CategoryNotFoundError(id)

    async def get_by_id(self, category_id: int) -> Optional[CategorySchema]:
        async with self.uow:
            res = await self.uow.category.get(id=category_id)
            self.check_result(category_id, res)
            return res.to_schema()

    async def create(self, product: CategoryCreateSchema) -> CategorySchema:
        async with self.uow:
            res = await self.uow.category.create(**product.model_dump(exclude_unset=True))
            await self.uow.commit()
            return res.to_schema()

    async def update(self, category_id: int, product: CategoryUpdateSchema) -> CategorySchema:
        async with self.uow:
            res = await self.uow.category.update(id=category_id, **product.model_dump(exclude_none=True))
            self.check_result(category_id, res)
            await self.uow.commit()
            return res.to_schema()

    async def delete(self, category_id: int) -> CategorySchema:
        async with self.uow:
            res = await self.uow.category.delete(id=category_id)
            self.check_result(category_id, res)
            await self.uow.commit()
            return res.to_schema()

    async def search(self, query: str) -> List[CategorySchema]:
        async with self.uow:
            res = await self.uow.category.search(query)
            return [e.to_schema() for e in res]
