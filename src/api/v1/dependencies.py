from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from core.config import settings
from db.unitofwork import InterfaceUnitOfWork, UnitOfWork
from exceptions.common import InvalidTokenError, UnauthorizedError
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
    try:
        payload = jwt.decode(token, settings.app.secret_key, algorithms=[settings.auth.algorithm])
    except JWTError:
        raise InvalidTokenError

    try:
        return AdminSchema(**payload)
    except ValueError:
        raise InvalidTokenError


UOWDep = Annotated[InterfaceUnitOfWork, Depends(UnitOfWork)]
AdminAuthDep = Annotated[AdminSchema, Depends(admin_auth)]
UserAuthDep = Annotated[WebAppInitData, Depends(user_auth)]
