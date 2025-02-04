import logging
from typing import Any, Dict, List, Optional, Tuple, Type
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .abstract import AbstractRepository, T


class SQLAlchemyRepository(AbstractRepository[T]):
    model: Type[T] = None

    def __init__(self, session: AsyncSession, model: Optional[Type[T]] = None) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.session = session
        if model is not None:
            self.model = model

    async def create(self, **data: Any) -> T:
        self.logger.debug(f'Creating with {data=}')
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.unique().scalar_one()

    async def get(self, **filter_by: Any) -> Optional[T]:
        self.logger.debug(f'Getting with {filter_by=}')
        stmt = select(self.model).filter_by(**filter_by).options(selectinload('*'))
        res = await self.session.execute(stmt)
        res = res.scalar_one_or_none()
        return res

    async def get_or_crete(self, defaults: Dict[str, Any], **filter_by: Any) -> Tuple[T, bool]:
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.scalar_one_or_none()
        if res is not None:
            self.logger.debug(f'Getting with {filter_by=}')
            return res, False

        defaults.update(filter_by)
        return await self.create(**defaults), True

    async def update(self, id: int, **values: Any) -> T:
        self.logger.debug(f'Updating with {id=} {values=}')
        stmt = update(self.model).where(self.model.id == id).values(**values).\
            options(selectinload('*')).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def delete(self, id: int) -> T:
        self.logger.debug(f'Deleting with {id=}')
        stmt = delete(self.model).filter_by(id=id).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def select(self, **filer_by: Any) -> List[T]:
        self.logger.debug(f'Selecting with {filer_by=}')
        stmt = select(self.model).filter_by(**filer_by).options(selectinload('*'))
        res = await self.session.execute(stmt)
        return res.scalars().all()
