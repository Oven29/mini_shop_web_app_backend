from typing import Any, List, Optional, Tuple, Type
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .abstract import AbstractRepository, T


class SQLAlchemyRepository(AbstractRepository[T]):
    model: Type[T] = None

    def __init__(self, session: AsyncSession, model: Optional[Type[T]] = None) -> None:
        self.session = session
        if model is not None:
            self.model = model

    async def create(self, **data: Any) -> T:
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get(self, **filter_by: Any) -> Optional[T]:
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.scalar_one_or_none()
        return res

    async def get_or_crete(self, defaults, **filter_by) -> Tuple[T, bool]:
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.scalar_one_or_none()
        if res:
            return res, False
        stmt = insert(self.model).values(**defaults).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one(), True

    async def update(self, id: int, **filter_by: Any) -> T:
        stmt = update(self.model).where(T.id == id).values(**filter_by).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def delete(self, id: int) -> T:
        stmt = delete(self.model).filter_by(id=id).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def select(self, **filer_by: Any) -> List[T]:
        stmt = select(self.model).filter_by(**filer_by)
        res = await self.session.execute(stmt)
        return res.scalars().all()
