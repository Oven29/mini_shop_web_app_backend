import logging
from typing import Optional
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

from core.config import settings
from utils.other import to_snake_case


engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

logger = logging.getLogger(__name__)


class Base(DeclarativeBase, AsyncAttrs):
    __abstract__ = True
    __schema__: BaseModel = None

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f'{to_snake_case(cls.__name__)}s'

    def to_schema(self) -> Optional[BaseModel]:
        if self.__schema__ is None:
            return

        fields = {}
        instance_values = vars(self)
        for field in self.__schema__.model_fields.keys():
            if field not in instance_values:
                continue
            value = instance_values[field]
            if isinstance(value, Base):
                value = value.to_schema()
            fields[field] = value

        logger.debug(f'Autogenerating schema {self.__class__.__name__} {fields=} {instance_values=}')
        return self.__schema__(**fields)


async def get_async_session():
    async with async_session_maker() as session:
        yield session
