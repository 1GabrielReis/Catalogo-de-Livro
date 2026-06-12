from abc import ABC , abstractmethod
from typing import List

from .api_biblioteca.livro_dto_response import Livro_dto_response
from .api_ia.ia_dto_response import IA_dto_response
from models.entities.livro import Livro

class IIa_interface(ABC):
    
    @abstractmethod
    def about_book(self,livro : Livro_dto_response|Livro) -> IA_dto_response:
        pass

class IBiblioteca_interface(ABC):
    
    @abstractmethod
    def findById(self,id: int) -> Livro_dto_response:
        pass

    @abstractmethod
    def findByTitle(self,title: str) -> List[Livro_dto_response]:
        pass

