from typing import List, TypeVar, Generic

from ..models.entities.livro import Livro
from ..schemas import Livro_schema
from ..models.dao.implementation.interface_Dao import Interface_Dao
from .service_exception import Service_Exception

class Livro_service:
    def __init__(self, repository:Interface_Dao[Livro]):
        self.repository = repository
    

    def insert(self,livro_schema: Livro_schema) -> int:
        try:
            livro = Livro(**livro_schema.model_dump())
            return self.repository.insert(livro)
        except Exception as erro:
            raise Service_Exception(f'erro insert service: \ninfo: {erro}')



    def update(self,livro_schema: Livro_schema) -> bool:
        try:
            livro = Livro(**livro_schema.model_dump())
            return self.repository.update(livro)
        except Exception as erro:
            raise Service_Exception(f'erro update service: \ninfo: {erro}')


    def deleteById(self, id: int) -> bool:
        try:
            return self.repository.deleteById(id)
        except Exception as erro:
            raise Service_Exception(f'erro deleteById service: \ninfo: {erro}')


    def findById(self, id: int) -> Livro:
        try:
            return self.repository.findById(id)
        except Exception as erro:
            raise Service_Exception(f'erro findById service: \ninfo: {erro}')


    def findAll(self) -> List[Livro]:
        try:
            return self.repository.findAll()
        except Exception as erro:
            raise Service_Exception(f'erro findAll service: \ninfo: {erro}')