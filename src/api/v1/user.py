from typing import List
from fastapi import APIRouter

from exceptions.admin import InvalidTokenError
from exceptions.common import UnauthorizedError
from schemas.user import UserSchema
from services.user import UserService
from schemas.order import OrderSchema
from .dependencies import AdminAuthDep, UserAuthDep, UOWDep


router = APIRouter(
    prefix='/user',
    tags=['user'],
)


@router.post(
    '/auth',
    responses={
        UnauthorizedError.status_code: UnauthorizedError.error_schema,
    },
)
async def auth(
    uow: UOWDep,
    user: UserAuthDep,
) -> UserSchema:
    return await UserService(uow).auth(user)


@router.post(
    '/get_all',
    responses={
        InvalidTokenError.status_code: InvalidTokenError.error_schema,
    }
)
async def get_all(
    uow: UOWDep,
    _: AdminAuthDep,
) -> List[UserSchema]:
    return await UserService(uow).get_all()


@router.post(
    '/get_orders',
    responses={
        UnauthorizedError.status_code: UnauthorizedError.error_schema,
    }
)
async def get_orders(
    uow: UOWDep,
    user: UserAuthDep,
) -> List[OrderSchema]:
    return await UserService(uow).get_orders(user)
