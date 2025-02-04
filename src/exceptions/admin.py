from fastapi import status

from .base import BaseApiError


class IncorrectUsernameOrPasswordError(BaseApiError):
    class Model(BaseApiError.Model):
        status_code: int = status.HTTP_401_UNAUTHORIZED
        msg: str = 'Incorrect username or password'


class LoginAlreadyExistsError(BaseApiError):
    class Model(BaseApiError.Model):
        status_code: int = status.HTTP_409_CONFLICT
        msg: str = 'Login already exists'
