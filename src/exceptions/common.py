from fastapi import status

from .base import BaseApiError


class UnauthorizedError(BaseApiError):
    class Model(BaseApiError.Model):
        status_code: int = status.HTTP_401_UNAUTHORIZED
        msg: str = 'Unauthorized'


class BadRequestError(BaseApiError):
    class Model(BaseApiError.Model):
        status_code: int = status.HTTP_400_BAD_REQUEST
        msg: str = 'Bad request'


class UnknownError(BaseApiError):
    class Model(BaseApiError.Model):
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
        msg: str = 'Unknown error'
