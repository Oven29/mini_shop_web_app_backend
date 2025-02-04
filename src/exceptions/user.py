from fastapi import status

from .base import BaseApiError


class WrongAuthData(BaseApiError):
    class Model(BaseApiError.Model):
        status_code: int = status.HTTP_401_UNAUTHORIZED
        msg: str = 'Wrong auth data'
