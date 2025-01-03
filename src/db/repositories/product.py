from typing import Any, Dict

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


class CategoryRepository(CommonRepository[Category]):
    model = Category


class ProductRepository(CommonRepository[Product]):
    model = Product

    async def create(self, **data: Any) -> Product:
        media = data.pop('media') if 'media' in data else []
        created = await super().create(**data)
        product_image = SQLAlchemyRepository[ProductImage](self.session, ProductImage)
        for item in media:
            await product_image.create(product_id=created.id, media_id=item.id)
        return created
