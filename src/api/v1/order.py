### TODO: implement

from fastapi import APIRouter

from .dependencies import AdminAuthDep, UserAuthDep, UOWDep


router = APIRouter(
    prefix='/order',
    tags=['order'],
)


@router.put('/reserve')
async def reserve(
    uow: UOWDep,
    user: UserAuthDep,
):
    return


@router.post('/cancel/{order_id}')
async def cancel(
    uow: UOWDep,
    user: UserAuthDep,
    order_id: int,
):
    pass


@router.post('/get/{order_id}')
async def get(
    uow: UOWDep,
    user: UserAuthDep,
    order_id: int,
):
    return


@router.post('/get_all')
async def get_all(
    uow: UOWDep,
    _: AdminAuthDep,
):
    return


@router.post('/delete/{order_id}')
async def delete(
    uow: UOWDep,
    _: AdminAuthDep,
    order_id: int,
):
    return
