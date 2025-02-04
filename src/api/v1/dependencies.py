from typing import Annotated, Optional
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from jwt.exceptions import PyJWTError

from core.config import settings
from db.unitofwork import InterfaceUnitOfWork, UnitOfWork
from exceptions.common import InvalidTokenError
from exceptions.user import WrongAuthData
from schemas.admin import AdminSchema
from schemas.user import UserSchema
from utils.validate import decode_admin_access_token, decode_user_access_token


def check_length_token(token: str) -> bool:
    return len(token.encode('utf-8')) <= settings.auth.max_token_size


async def user_token_depend(request: Request) -> str:
    authorization = request.headers.get("Authorization")
    scheme, param = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        raise InvalidTokenError

    return param


def user_auth(token: Annotated[str, Depends(user_token_depend)]) -> UserSchema:
    if not check_length_token(token):
        raise InvalidTokenError

    try:
        return decode_user_access_token(token)
    except (PyJWTError, ValueError):
        raise InvalidTokenError


oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/v1/admin/login', auto_error=False)


def admin_auth(token: Annotated[Optional[str], Depends(oauth2_bearer)]) -> AdminSchema:
    if token is None:
        raise InvalidTokenError

    if not check_length_token(token):
        raise InvalidTokenError

    try:
        return decode_admin_access_token(token)
    except (PyJWTError, ValueError):
        raise InvalidTokenError


UOWDep = Annotated[InterfaceUnitOfWork, Depends(UnitOfWork)]
AdminAuthDep = Annotated[AdminSchema, Depends(admin_auth)]
UserAuthDep = Annotated[UserSchema, Depends(user_auth)]
