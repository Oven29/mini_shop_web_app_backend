from fastapi import status

from .base import BaseException


class InvalidTokenError(BaseException):
    message = 'Invalid token'
    status_code = status.HTTP_401_UNAUTHORIZED


class UnauthorizedError(BaseException):
    message = 'Unauthorized'
    status_code = status.HTTP_401_UNAUTHORIZED
