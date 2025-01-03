from typing import List
from fastapi import APIRouter, HTTPException, status

from schemas.product import ProductSchema, ProductCreateSchema, ProductUpdateSchema
from services.product import ProductService
from .dependencies import UOWDep, AdminAuthDep


router = APIRouter(
    prefix='/product',
    tags=['product'],
)


def check_exists_product(res: ProductSchema | None) -> ProductSchema:
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='404 - Product not found',
        )
    return res


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
    res = await ProductService(uow).get_by_id(product_id)
    return check_exists_product(res)


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
    res = await ProductService(uow).update(product_id, product)
    return check_exists_product(res)


@router.delete('/delete')
async def delete(
    uow: UOWDep,
    _: AdminAuthDep,
    product_id: int,
) -> ProductSchema:
    res = await ProductService(uow).delete(product_id)
    return check_exists_product(res)
