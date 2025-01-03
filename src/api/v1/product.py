from typing import List
from fastapi import APIRouter

from schemas.product import ProductDeleteSchema, ProductSchema, ProductCreateSchema, ProductUpdateSchema
from .dependencies import UOWDep, AdminAuthDep, UserAuthDep


router = APIRouter(
    prefix='/product',
    tags=['product'],
)


@router.get('/get_all')
async def get_all(
    uow: UOWDep,
    user: UserAuthDep,
) -> List[ProductSchema]:
    pass


@router.get('/get_by_id')
async def get_by_id(
    uow: UOWDep,
    user: UserAuthDep,
) -> ProductSchema:
    pass


@router.post('/create')
async def create(
    uow: UOWDep,
    admin: AdminAuthDep,
    product: ProductCreateSchema,
) -> ProductSchema:
    pass


@router.put('/update')
async def update(
    uow: UOWDep,
    admin: AdminAuthDep,
    product: ProductUpdateSchema,
) -> ProductSchema:
    pass


@router.delete('/delete')
async def delete(
    uow: UOWDep,
    admin: AdminAuthDep,
    product: ProductDeleteSchema,
) -> ProductSchema:
    pass
