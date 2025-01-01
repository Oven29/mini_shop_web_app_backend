from typing import Any, Dict

from src.utils.other import get_translit
from .base import SQLAlchemyRepository, T
from ..models.product import Product, Category


class CommonRepository(SQLAlchemyRepository):
    def create(self, **data: Any) -> T:
        if 'translit' not in data:
            data['translit'] = get_translit(data['name'])
        return super().create(**data)

    def get_or_crete(self, defaults: Dict[str, Any], **filter_by: Any) -> T:
        if 'translit' not in defaults:
            defaults['translit'] = get_translit(defaults['name'])
        return super().get_or_crete(defaults, **filter_by)


class CategoryRepository(CommonRepository[Category]):
    pass


class ProductRepository(CommonRepository[Product]):
    pass
