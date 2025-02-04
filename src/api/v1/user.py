from typing import List
from fastapi import APIRouter

from exceptions.common import InvalidTokenError
from exceptions.user import WrongAuthData
from schemas.common import TokenSchema
from schemas.user import UserAuthSchema, UserSchema
from services.user import UserService
from schemas.order import OrderSchema
from utils.validate import create_user_access_token
from .dependencies import AdminAuthDep, UserAuthDep, UOWDep


router = APIRouter(
    prefix='/user',
    tags=['user'],
)


@router.post(
    '/auth',
    responses={
        WrongAuthData.status_code: WrongAuthData.error_schema,
    },
)
async def auth(
    uow: UOWDep,
    user_auth: UserAuthSchema,
) -> TokenSchema:
    user = await UserService(uow).auth(user_auth)
    token = create_user_access_token(user)
    return TokenSchema(access_token=token, token_type='bearer')


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
        InvalidTokenError.status_code: InvalidTokenError.error_schema,
    }
)
async def get_orders(
    uow: UOWDep,
    user: UserAuthDep,
) -> List[OrderSchema]:
    return await UserService(uow).get_orders(user)
