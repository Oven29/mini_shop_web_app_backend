from fastapi import APIRouter

from .product import router as product_router
from .category import router as category_router
from .admin import router as admin_router
from .user import router as user_router

v1_router = APIRouter(
    prefix='/v1',
)

v1_router.include_router(product_router)
v1_router.include_router(category_router)
v1_router.include_router(admin_router)
v1_router.include_router(user_router)
