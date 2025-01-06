from abc import ABC, abstractmethod
import os
from typing import Type
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from core.config import settings

from .base import async_session_maker
from .repositories.admin import AdminRepository
from .repositories.media import MediaRepository
from .repositories.order import OrderRepository, InvoiceRepository
from .repositories.product import CategoryRepository, ProductRepository
from .repositories.user import UserRepository


class InterfaceUnitOfWork(ABC):
    admin: Type[AdminRepository]
    media: Type[MediaRepository]
    order: Type[OrderRepository]
    invoice: Type[InvoiceRepository]
    category: Type[CategoryRepository]
    product: Type[ProductRepository]
    user: Type[UserRepository]

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class UnitOfWork(InterfaceUnitOfWork):
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.admin = AdminRepository(self.session)
        self.media = MediaRepository(self.session)
        self.order = OrderRepository(self.session)
        self.invoice = InvoiceRepository(self.session)
        self.category = CategoryRepository(self.session)
        self.product = ProductRepository(self.session)
        self.user = UserRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


class TestUnitOfWork(UnitOfWork):
    def __init__(self):
        engine = create_async_engine('sqlite+aiosqlite:///' + os.path.join(settings.dir.base, 'test.sqlite'))
        self.session_factory = async_sessionmaker(engine, expire_on_commit=False)
        
