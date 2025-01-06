from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt

from core.config import settings
from db.unitofwork import InterfaceUnitOfWork, UnitOfWork
from exceptions.admin import InvalidTokenError
from exceptions.common import UnauthorizedError
from schemas.admin import AdminSchema
from schemas.user import WebAppInitData, UserSchema
from utils.validate import validate_user_init_data


def user_auth(init_data: WebAppInitData) -> UserSchema:
    if not validate_user_init_data(init_data):
        raise UnauthorizedError

    return UserSchema(
        user_id=init_data.user.id,
        username=init_data.user.username,
        first_name=init_data.user.first_name,
    )


oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/v1/admin/login')


def admin_auth(token: Annotated[str, Depends(oauth2_bearer)]) -> AdminSchema:
    if len(token.encode('utf-8')) > settings.auth.max_token_size:
        raise InvalidTokenError

    try:
        payload = jwt.decode(token, settings.app.secret_key.get_secret_value(), algorithms=[settings.auth.algorithm])
    except jwt.exceptions.PyJWTError:
        raise InvalidTokenError

    try:
        id, login = payload['sub'].split('_', 1)
        return AdminSchema(id=int(id), login=login)
    except ValueError:
        raise InvalidTokenError


UOWDep = Annotated[InterfaceUnitOfWork, Depends(UnitOfWork)]
AdminAuthDep = Annotated[AdminSchema, Depends(admin_auth)]
UserAuthDep = Annotated[WebAppInitData, Depends(user_auth)]
