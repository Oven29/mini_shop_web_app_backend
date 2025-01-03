from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, Tuple, TypeVar

from ...base import Base


T = TypeVar('T', bound=Base)


class AbstractRepository(ABC, Generic[T]):
    """Abstract class for repositories"""

    @abstractmethod
    async def create(self, **data: Any) -> T:
        """
        Create new record

        :param data: data for create
        :return: created record
        """
        raise NotImplementedError

    @abstractmethod
    async def get(self, **filter_by: Any) -> Optional[T]:
        """
        Get record by filter if exists, else return None

        :param filter_by: filter for get record
        :return: record or None
        """
        raise NotImplementedError

    @abstractmethod
    async def get_or_crete(self, defaults: Dict[str, Any], **filter_by: Any) -> Tuple[T, bool]:
        """
        Get record by filter if exists, else create new record

        :param defaults: data for create
        :param filter_by: filter for get record
        :return: record and created flag
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, **filter_by: Any) -> T:
        """
        Update record by id

        :param id: record id
        :param filter_by: data for update
        :return: updated record or None
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> T:
        """
        Delete record by id

        :param id: record id
        :return: deleted record or None
        """
        raise NotImplementedError

    @abstractmethod
    async def select(self, **filter_by: Any) -> List[T]:
        """
        Select records by filter

        :param filter_by: filter for select records
        :return: list of records
        """
        raise NotImplementedError
