from fastapi import status

from .base import BaseApiError


class InvoiceNotFoundError(BaseApiError):
    class Model(BaseApiError.Model):
        status_code: int = status.HTTP_404_NOT_FOUND
        msg: str = 'Invoice with {pay_id=} not found'
        pay_id: str = ''

    def __init__(self, pay_id: str) -> None:
        super().__init__(pay_id=pay_id)


class PaymentMethodNotFoundError(BaseApiError):
    class Model(BaseApiError.Model):
        status_code: int = status.HTTP_404_NOT_FOUND
        msg: str = 'Payment method with {name=} not found or disabled'
        name: str = ''

    def __init__(self, name: str) -> None:
        super().__init__(name=name)


class InvoiceForiddenError(BaseApiError):
    class Model(BaseApiError.Model):
        status_code: int = status.HTTP_403_FORBIDDEN
        msg: str = 'Invoice foridden'
