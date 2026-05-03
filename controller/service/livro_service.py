from typing import List, TypeVar, Generic

from ...models.entities.livro import Livro
from ...models.dao.implementation.interface_Dao import Interface_Dao

class Livro_service:
    def __init__(self, repository:Interface_Dao[Livro]):
        self.repository = repository
    

    def insert(self,livro: Livro) -> int:
        pass


    def update(self,livro: Livro) -> bool:
        pass


    def deleteById(self, id: int) -> bool:
        pass


    def findById(self, id: int) -> Livro:
        pass


    def findAll(self) -> List[Livro]:
        pass