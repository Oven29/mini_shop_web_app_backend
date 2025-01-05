from fastapi import status

from .base import BaseException


class IncorrectUsernameOrPasswordError(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = 'Incorrect username or password'


class LoginAlreadyExistsError(BaseException):
    status_code = status.HTTP_409_CONFLICT
    message = 'Login already exists'


class InvalidTokenError(BaseException):
    message = 'Invalid token'
    status_code = status.HTTP_401_UNAUTHORIZED
