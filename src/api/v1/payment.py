from fastapi import APIRouter

from .dependencies import AdminAuthDep, UserAuthDep, UOWDep


router = APIRouter(
    prefix='/payment',
    tags=['payment'],
)


@router.get('/get_methods')
async def get_methods(
    uow: UOWDep,
    user: UserAuthDep,
):
    return


@router.put('/create_invoice')
async def create_invoice(
    uow: UOWDep,
    user: UserAuthDep,
):
    return


@router.post('/get_invoice')
async def get_invoice(
    uow: UOWDep,
    user: UserAuthDep,
):
    """Get by user"""
    return


@router.get('/get')
async def get(
    uow: UOWDep,
    admin: AdminAuthDep,
):
    """Get by admin"""
    return


@router.post('/webhook')
async def paymant_webhook(
    uow: UOWDep,
):
    return
