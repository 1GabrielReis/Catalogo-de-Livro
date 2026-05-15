from typing import List, TypeVar, Generic

from ..models.entities.livro import Livro
from ..schemas import Livro_schema
from ..models.dao.livro_interface import ILivro_interface
from .service_exception import Service_Exception

class Livro_service:
    def __init__(self, repository:ILivro_interface[Livro]):
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
        
    def _format_book(self, livro:Livro_schema):
        return Livro(id= livro.id.strip() if livro.id else None,
                     titulo= " ".join([palavra.title() for palavra in livro.titulo.split()]),
                     autor= " ".join([nome.title() for nome in livro.autor.split()]),
                     editora= " ".join([empresa.lower() for empresa in livro.editora.split()]),
                     sobre= livro.sobre.strip() if livro.sobre else None,
                     data_criacao= livro.data_criacao)