from typing import List
from fastapi import APIRouter, HTTPException, status

from exceptions.product import ProductNotFoundError
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
    try:
        return await ProductService(uow).get_by_id(product_id)
    except ProductNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'404 - {e.message}',
        )


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
    try:
        return await ProductService(uow).update(product_id, product)
    except ProductNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'404 - {e.message}',
        )


@router.delete('/delete')
async def delete(
    uow: UOWDep,
    _: AdminAuthDep,
    product_id: int,
) -> ProductSchema:
    try:
        return await ProductService(uow).delete(product_id)
    except ProductNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'404 - {e.message}',
        )
