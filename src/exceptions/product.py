from fastapi import status

from .base import BaseException


class ProductNotFoundError(BaseException):
    def __init__(self, id: int):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.message = f'Product with {id=} not found'
        super().__init__(self.message)
