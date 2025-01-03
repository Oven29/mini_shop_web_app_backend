from typing import Any, Dict, List, Optional

from sqlalchemy import select

from utils.other import get_translit
from .base import SQLAlchemyRepository, T
from ..models.product import Product, Category, ProductImage


class CommonRepository(SQLAlchemyRepository[T]):
    async def create(self, **data: Any) -> T:
        if 'translit' not in data:
            data['translit'] = get_translit(data['name'])[256:]

        return await super().create(**data)

    async def get_or_crete(self, defaults: Dict[str, Any], **filter_by: Any) -> T:
        if 'translit' not in defaults and 'translit' not in filter_by:
            name = defaults.get('name') or filter_by.get('name')
            if name:
                defaults['translit'] = get_translit(name)[256:]

        return await super().get_or_crete(defaults, **filter_by)

    async def search(self, query: str) -> List[T]:
        """
        Search by name, translit or by id

        :param query: search query
        :return: list of records
        """
        res = []
        if query.isdigit() and (item := await self.get(id=int(query))) is not None:
            res.append(item)

        searching_query = f'%{query.strip().lower()}%'
        stmt = select(self.model).filter(
            self.model.name.ilike(searching_query) | self.model.translit.ilike(searching_query)
        )
        response = await self.session.execute(stmt)
        return res + response.scalars().all()


class CategoryRepository(CommonRepository[Category]):
    model = Category


class ProductRepository(CommonRepository[Product]):
    model = Product

    def get_product_image_repository(self) -> SQLAlchemyRepository:
        return SQLAlchemyRepository[ProductImage](self.session, ProductImage)

    async def create(self, **data: Any) -> Product:
        media = data.pop('media') if 'media' in data else []
        created = await super().create(**data)
        product_image = self.get_product_image_repository()
        for item in media:
            await product_image.create(product_id=created.id, media_id=item.id)
        return created

    async def update(self, id: int, **values: Any) -> Optional[Product]:
        if 'media' in values:
            product_image = self.get_product_image_repository()
            items = await product_image.select(product_id=id)
            for el in items:
                await product_image.delete(el.id)
            media = values.pop('media')
            for item in media:
                await product_image.create(product_id=id, media_id=item)

        return await super().update(id, **values)
