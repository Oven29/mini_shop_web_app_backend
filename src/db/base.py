import logging
from typing import Any, List, Optional
from pydantic import BaseModel
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

from core.config import settings
from utils.other import to_snake_case


engine = create_async_engine(settings.db.url.get_secret_value(), echo=settings.app.debug)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

logger = logging.getLogger(__name__)


class Base(DeclarativeBase, AsyncAttrs):
    __abstract__ = True
    __schema__: BaseModel = None

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f'{to_snake_case(cls.__name__)}s'

    async def to_schema(self, **kwargs: Any) -> Optional[BaseModel]:
        if self.__schema__ is None:
            return

        fields = kwargs.copy()
        fields.update({
            field: getattr(self, field)
              for field in self.__schema__.model_fields.keys()
              if hasattr(self, field)
        })

        logger.debug(f'Autogenerating schema {self.__class__.__name__} {fields=}')
        return self.__schema__(**fields)

    def __bool__(self) -> bool:
        return True

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} id={self.id}>'


async def get_async_session():
    async with async_session_maker() as session:
        yield session
