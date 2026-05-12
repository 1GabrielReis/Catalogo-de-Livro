from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic

T = TypeVar('T')

class Interface_Dao(ABC,Generic[T]):
    
    @abstractmethod
    def insert(self,entity: T):
        pass

    @abstractmethod
    def update(self,entity: T) -> bool:
        pass

    @abstractmethod
    def deleteById(self, id: str) -> bool:
        pass

    @abstractmethod
    def findById(self, id: str) -> T:
        pass

    @abstractmethod
    def findAll(self) -> List[T]:
        pass
