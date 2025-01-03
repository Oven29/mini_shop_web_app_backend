from fastapi import APIRouter

from .product import router as product_router

v1_router = APIRouter(
    prefix='/v1',
    tags=['v1'],
)

v1_router.include_router(product_router)
