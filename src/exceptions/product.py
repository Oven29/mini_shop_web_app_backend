from fastapi import status

from .base import BaseException


class ProductNotFoundError(BaseException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, id: int):
        self.message = f'Product with {id=} not found'
        super().__init__(self.message)
