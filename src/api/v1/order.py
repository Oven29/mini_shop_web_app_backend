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


@router.post('/confirm')
async def confirm(
    uow: UOWDep,
    user: UserAuthDep,
):
    return


@router.post('/cancel')
async def cancel(
    uow: UOWDep,
    user: UserAuthDep,
):
    pass


@router.post('/get')
async def get(
    uow: UOWDep,
    user: UserAuthDep,
):
    return


@router.post('/get_all')
async def get_all(
    uow: UOWDep,
    _: AdminAuthDep,
):
    return


@router.post('/delete')
async def delete(
    uow: UOWDep,
    _: AdminAuthDep,
    order_id: int,
):
    return
