from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from exceptions.admin import LoginAlreadyExistsError, IncorrectUsernameOrPasswordError
from exceptions.common import InvalidTokenError
from schemas.admin import AdminSchema, AdminCreateSchema
from schemas.common import TokenSchema
from services.admin import AdminService
from utils.validate import create_admin_access_token
from .dependencies import UOWDep, AdminAuthDep


router = APIRouter(
    prefix='/admin',
    tags=['admin'],
)


@router.post(
    '/login',
    responses={
        IncorrectUsernameOrPasswordError.status_code: IncorrectUsernameOrPasswordError.error_schema,
    },
)
async def login(
    uow: UOWDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenSchema:
    admin = await AdminService(uow).login(form_data.username, form_data.password)
    token = create_admin_access_token(admin)
    return TokenSchema(access_token=token, token_type='bearer')


@router.put(
    '/create_admin',
    responses={
        InvalidTokenError.status_code: InvalidTokenError.error_schema,
        LoginAlreadyExistsError.status_code: LoginAlreadyExistsError.error_schema,
    },
)
async def create_admin(
    uow: UOWDep,
    _: AdminAuthDep,
    admin: AdminCreateSchema,
) -> AdminSchema:
    return await AdminService(uow).create(admin)
