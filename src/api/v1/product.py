from typing import List
from fastapi import APIRouter

from schemas.product import ProductSchema, ProductCreateSchema, ProductUpdateSchema
from services.product import ProductService
from .dependencies import UOWDep, AdminAuthDep


router = APIRouter(
    prefix='/product',
    tags=['product'],
)


@router.get('/get_all')
async def get_all(
    uow: UOWDep,
) -> List[ProductSchema]:
    return await ProductService(uow).get_all()


@router.get('/get_by_id')
async def get_by_id(
    uow: UOWDep,
    product_id: int,
) -> ProductSchema:
    return await ProductService(uow).get_by_id(product_id)


@router.get('/search')
async def search(
    uow: UOWDep,
    query: str,
) -> List[ProductSchema]:
    return await ProductService(uow).search(query)


@router.post('/create')
async def create(
    uow: UOWDep,
    _: AdminAuthDep,
    product: ProductCreateSchema,
) -> ProductSchema:
    return await ProductService(uow).create(product)


@router.put('/update')
async def update(
    uow: UOWDep,
    _: AdminAuthDep,
    product_id: int,
    product: ProductUpdateSchema,
) -> ProductSchema:
    return await ProductService(uow).update(product_id, product)


@router.delete('/delete')
async def delete(
    uow: UOWDep,
    _: AdminAuthDep,
    product_id: int,
) -> ProductSchema:
    return await ProductService(uow).delete(product_id)
