from typing import List
from fastapi import APIRouter

from schemas.category import CategorySchema, CategoryCreateSchema, CategoryUpdateSchema
from schemas.product import ProductSchema
from services.category import CategoryService
from .dependencies import UOWDep, AdminAuthDep


router = APIRouter(
    prefix='/category',
    tags=['category'],
)


@router.get('/get_all')
async def get_all(
    uow: UOWDep,
) -> List[CategorySchema]:
    return await CategoryService(uow).get_all()


@router.get('/get_by_id')
async def get_by_id(
    uow: UOWDep,
    category_id: int,
) -> CategorySchema:
    return await CategoryService(uow).get_by_id(category_id)


@router.get('/get_products', tags=['product'])
async def get_products(
    uow: UOWDep,
    category_id: int,
) -> List[ProductSchema]:
    return await CategoryService(uow).get_products(category_id)


@router.post('/create')
async def create(
    uow: UOWDep,
    _: AdminAuthDep,
    product: CategoryCreateSchema,
) -> CategorySchema:
    return await CategoryService(uow).create(product)


@router.put('/update')
async def update(
    uow: UOWDep,
    _: AdminAuthDep,
    category_id: int,
    product: CategoryUpdateSchema,
) -> CategorySchema:
    return await CategoryService(uow).update(category_id, product)


@router.delete('/delete')
async def delete(
    uow: UOWDep,
    _: AdminAuthDep,
    category_id: int,
) -> CategorySchema:
    return await CategoryService(uow).delete(category_id)
