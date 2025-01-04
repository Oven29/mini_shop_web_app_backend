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


@router.post('/get/{invoice_id}')
async def get_invoice_by_user(
    uow: UOWDep,
    user: UserAuthDep,
):
    return


@router.get('/get/{invoice_id}')
async def get_invoice_by_admin(
    uow: UOWDep,
    admin: AdminAuthDep,
):
    return


@router.post('/webhook/{method}')
async def payment_webhook(
    uow: UOWDep,
    method: str,
):
    return
