from enum import Enum


class InvoiceStatus(str, Enum):
    WAIT = 'WAIT'
    PAID = 'PAID'
    CANCEL = 'CANCEL'


class OrderStatus(str, Enum):
    RESERVE = 'RESERVE'
    CANCEL = 'CANCEL'
    DELIVERY = 'DELIVERY'
    DONE = 'DONE'
