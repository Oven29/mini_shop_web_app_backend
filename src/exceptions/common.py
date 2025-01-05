from fastapi import status

from .base import BaseException


class InvalidTokenError(BaseException):
    message = 'Invalid token'
    status_code = status.HTTP_401_UNAUTHORIZED


class UnauthorizedError(BaseException):
    message = 'Unauthorized'
    status_code = status.HTTP_401_UNAUTHORIZED


class BadRequestError(BaseException):
    message = 'Bad request'
    status_code = status.HTTP_400_BAD_REQUEST


class UnknownError(BaseException):
    message = 'Unknown error'
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
