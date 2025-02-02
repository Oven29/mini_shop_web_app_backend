from typing import Annotated
from fastapi import Depends, Header
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import PyJWTError

from core.config import settings
from db.unitofwork import InterfaceUnitOfWork, UnitOfWork
from exceptions.admin import InvalidTokenError
from exceptions.common import UnauthorizedError
from schemas.admin import AdminSchema
from schemas.user import UserAuthHeader, UserSchema
from utils.validate import validate_user_init_data, decode_admin_access_token


def user_auth(user_auth: UserAuthHeader = Header()) -> UserSchema:
    if not validate_user_init_data(user_auth.init_data):
        raise UnauthorizedError

    return UserSchema(
        user_id=user_auth.init_data.user.id,
        username=user_auth.init_data.user.username,
        first_name=user_auth.init_data.user.first_name,
    )


oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/v1/admin/login')


def admin_auth(token: Annotated[str, Depends(oauth2_bearer)]) -> AdminSchema:
    if len(token.encode('utf-8')) > settings.auth.max_token_size:
        raise InvalidTokenError

    try:
        return decode_admin_access_token(token)
    except (PyJWTError, ValueError):
        raise InvalidTokenError


UOWDep = Annotated[InterfaceUnitOfWork, Depends(UnitOfWork)]
AdminAuthDep = Annotated[AdminSchema, Depends(admin_auth)]
UserAuthDep = Annotated[UserSchema, Depends(user_auth)]
