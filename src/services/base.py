from abc import ABC

from db.unitofwork import InterfaceUnitOfWork


class AbstractService(ABC):
    def __init__(self, uow: InterfaceUnitOfWork) -> None:
        self.uow: InterfaceUnitOfWork = uow
