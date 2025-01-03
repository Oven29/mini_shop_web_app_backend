from fastapi import status

from .base import BaseException


class InvalidToken(BaseException):
    message = 'Invalid token'
    status_code = status.HTTP_401_UNAUTHORIZED


class Unauthorized(BaseException):
    message = 'Unauthorized'
    status_code = status.HTTP_401_UNAUTHORIZED
