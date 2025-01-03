from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from schemas.admin import AdminSchema, AdminCreateSchema, Token
from services.admin import AdminService
from utils.validate import create_admin_access_token
from .dependencies import UOWDep, AdminAuthDep


router = APIRouter(
    prefix='/admin',
    tags=['admin'],
)


@router.post('/login')
async def login(
    uow: UOWDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    admin = await AdminService(uow).login(form_data.username, form_data.password)
    token = create_admin_access_token(admin)
    return Token(access_token=token, token_type='bearer')


@router.put('/create_admin')
async def create_admin(
    uow: UOWDep,
    _: AdminAuthDep,
    admin: AdminCreateSchema,
) -> AdminSchema:
    return await AdminService(uow).create(admin)
