from typing import List
from fastapi import APIRouter, Request

from exceptions.admin import InvalidTokenError
from exceptions.common import BadRequestError, UnauthorizedError
from exceptions.payment import InvoiceForiddenError, InvoiceNotFoundError, PaymentMethodNotFoundError
from schemas.common import HttpOk
from schemas.payment import InvoiceSchema, InvoiceCreateSchema
from services.payment import PaymentService
from .dependencies import AdminAuthDep, UserAuthDep, UOWDep


router = APIRouter(
    prefix='/payment',
    tags=['payment'],
)


@router.get('/get_methods')
async def get_methods(
    uow: UOWDep,
) -> List[str]:
    return await PaymentService(uow).get_methods()


@router.put(
    '/create_invoice',
    responses={
        UnauthorizedError.status_code: UnauthorizedError.error_schema,
        PaymentMethodNotFoundError.status_code: PaymentMethodNotFoundError.error_schema,
    },
)
async def create_invoice(
    uow: UOWDep,
    user: UserAuthDep,
    data: InvoiceCreateSchema,
) -> InvoiceSchema:
    return await PaymentService(uow).create_invoice(data, user)


@router.post(
    '/get/{invoice_id}',
    responses={
        UnauthorizedError.status_code: UnauthorizedError.error_schema,
        InvoiceNotFoundError.status_code: InvoiceNotFoundError.error_schema,
        InvoiceForiddenError.status_code: InvoiceForiddenError.error_schema,
    },
)
async def get_invoice_by_user(
    uow: UOWDep,
    user: UserAuthDep,
    invoice_id: str,
) -> InvoiceSchema:
    await PaymentService(uow).get_invoice(invoice_id, user)


@router.get(
    '/get/{invoice_id}',
    responses={
        InvalidTokenError.status_code: InvalidTokenError.error_schema,
        InvoiceNotFoundError.status_code: InvoiceNotFoundError.error_schema,
    },
)
async def get_invoice_by_admin(
    uow: UOWDep,
    _: AdminAuthDep,
    invoice_id: str,
) -> InvoiceSchema:
    await PaymentService(uow).get_invoice(invoice_id)


@router.post(
    '/webhook/{method}',
    responses={
        BadRequestError.status_code: BadRequestError.error_schema,
        PaymentMethodNotFoundError.status_code: PaymentMethodNotFoundError.error_schema,
    },
)
async def payment_webhook(
    uow: UOWDep,
    request: Request,
    method: str,
) -> HttpOk:
    await PaymentService(uow).webhook(method, request)
    return HttpOk()
