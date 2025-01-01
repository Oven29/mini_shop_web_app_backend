from typing import Annotated
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from core.config import settings
from db.unitofwork import InterfaceUnitOfWork, UnitOfWork
from schemas.admin import AdminSchema
from schemas.user import WebAppInitData
from utils.validate import validate_user_init_data


def user_auth(init_data: WebAppInitData) -> WebAppInitData:
    if not validate_user_init_data(init_data):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='401 - Unauthorized',
        )

    return init_data


def admin_auth(token: str) -> AdminSchema:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='401 - Invalid token',
        )

    try:
        return AdminSchema(**payload)

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='401 - Invalid token',
        )


UOWDep = Annotated[InterfaceUnitOfWork, Depends(UnitOfWork)]
AdminAuthDep = Annotated[AdminSchema, Depends(admin_auth)]
UserAuthDep = Annotated[WebAppInitData, Depends(user_auth)]
