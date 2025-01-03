from fastapi import status

from .base import BaseException


class CategoryNotFoundError(BaseException):
    def __init__(self, id: int):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.message = f'Category with {id=} not found'
        super().__init__(self.message)
