from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic

class DB_base(ABC):
    @abstractmethod
    def getConn(**kwargs):
        pass
    @abstractmethod
    def closeCursor(entity):
        pass
    @abstractmethod
    def disconnect():
        pass