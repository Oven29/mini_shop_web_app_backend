from abc import ABC
import logging

from db.unitofwork import InterfaceUnitOfWork


class AbstractService(ABC):
    def __init__(self, uow: InterfaceUnitOfWork) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.uow: InterfaceUnitOfWork = uow
