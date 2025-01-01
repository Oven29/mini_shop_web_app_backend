from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, Tuple, TypeVar


T = TypeVar("T")


class AbstractRepository(ABC, Generic[T]):
    @abstractmethod
    async def create(self, **data: Any) -> T:
        raise NotImplementedError

    @abstractmethod
    async def get(self, **filter_by: Any) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    async def get_or_crete(self, defaults: Dict[str, Any], **filter_by: Any) -> Tuple[T, bool]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, **filter_by: Any) -> T:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> T:
        raise NotImplementedError

    @abstractmethod
    async def select(self, **filter_by: Any) -> List[T]:
        raise NotImplementedError
