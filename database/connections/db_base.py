from abc import ABC, abstractmethod
from typing import Any

class DB_base(ABC):
    @abstractmethod
    def getConn(self,**kwargs) -> Any :
        pass
    @abstractmethod
    def closeCursor(self,entity: Any):
        pass
    @abstractmethod
    def disconnect(self):
        pass