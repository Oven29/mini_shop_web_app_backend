from fastapi import status

from .base import BaseApiError


class CategoryNotFoundError(BaseApiError):
    class Model(BaseApiError.Model):
        status_code: int = status.HTTP_404_NOT_FOUND
        msg: str = 'Category with id={id} not found'
        id: int = 0

    def __init__(self, id: int) -> None:
        super().__init__(id=id)
