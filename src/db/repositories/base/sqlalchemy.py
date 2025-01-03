from typing import Any, List, Optional, Tuple
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .abstract import AbstractRepository, T


class SQLAlchemyRepository(AbstractRepository[T]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, **data: Any) -> T:
        stmt = insert(T).values(**data).returning(T.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get(self, **filter_by: Any) -> Optional[T]:
        stmt = select(T).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.scalar_one_or_none()
        return res

    async def get_or_crete(self, defaults, **filter_by) -> Tuple[T, bool]:
        stmt = select(T).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.scalar_one_or_none()
        if res:
            return res, False
        stmt = insert(T).values(**defaults).returning(T.id)
        res = await self.session.execute(stmt)
        return res.scalar_one(), True

    async def update(self, id: int, **filter_by: Any) -> T:
        stmt = update(T).where(T.id == id).values(**filter_by).returning(T.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def delete(self, id: int) -> T:
        stmt = delete(T).filter_by(id=id).returning(T.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def select(self, **filer_by: Any) -> List[T]:
        stmt = select(T).filter_by(**filer_by)
        res = await self.session.execute(stmt)
        return res.scalars().all()
