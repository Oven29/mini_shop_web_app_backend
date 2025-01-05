from fastapi import status

from .base import BaseException


class InvoiceNotFoundError(BaseException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, pay_id: str) -> None:
        self.message = f'Invoice with {pay_id=} not found'
        super().__init__(self.message)
