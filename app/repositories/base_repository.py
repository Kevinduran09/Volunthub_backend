from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional


T = TypeVar("T")  # Generic type model


class BaseRepository(ABC, Generic[T]):
    """
    Define the structure of all repositories that implement this base repository
    """
    @abstractmethod
    async def get_all(self) -> List[T]:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[T]:
        pass

    @abstractmethod
    async def create(self, entity: T) -> T:
        pass

    @abstractmethod
    async def update(self, id: int, entity: T) -> T:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        """
        Delete an entity by id.
        Returns True if the entity was deleted, False if it didn't exist.
        """
        pass
