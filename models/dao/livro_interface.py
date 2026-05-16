from abc import abstractmethod
from typing import List

from .dao_interface import IDao_interface
from ..entities.livro import Livro


class ILivro_interface(IDao_interface):
    
    @abstractmethod
    def findByTitle(self,title: str) -> List[Livro]:
        pass