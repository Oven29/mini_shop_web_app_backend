from typing import Annotated
from fastapi import Depends
from jose import JWTError, jwt

from core.config import settings
from db.unitofwork import InterfaceUnitOfWork, UnitOfWork
from exceptions.common import InvalidToken, Unauthorized
from schemas.admin import AdminSchema
from schemas.user import WebAppInitData
from utils.validate import validate_user_init_data


def user_auth(init_data: WebAppInitData) -> WebAppInitData:
    if not validate_user_init_data(init_data):
        raise Unauthorized

    return init_data


def admin_auth(token: str) -> AdminSchema:
    return AdminSchema(id=1, login='admin')
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise InvalidToken

    try:
        return AdminSchema(**payload)
    except ValueError:
        raise InvalidToken


UOWDep = Annotated[InterfaceUnitOfWork, Depends(UnitOfWork)]
AdminAuthDep = Annotated[AdminSchema, Depends(admin_auth)]
UserAuthDep = Annotated[WebAppInitData, Depends(user_auth)]
