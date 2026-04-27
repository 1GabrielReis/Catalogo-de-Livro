from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic

T = TypeVar('T')

class BaseDao(ABC,Generic[T]):
    
    @abstractmethod
    def insert(self,entity: T) -> int:
        pass

    @abstractmethod
    def update(self,entity: T) -> bool:
        pass

    @abstractmethod
    def deleteById(self, id) -> bool:
        pass

    @abstractmethod
    def findById(self, id) -> T:
        pass

    @abstractmethod
    def findAll(self) -> List[T]:
        pass
