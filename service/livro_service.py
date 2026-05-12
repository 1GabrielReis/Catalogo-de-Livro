from typing import List, TypeVar, Generic

from ..models.entities.livro import Livro
from ..schemas import Livro_schema
from ..models.dao.implementation.interface_Dao import Interface_Dao
from ..clients.clients_interface import IBiblioteca_interface, IIa_interface
from ..clients.api_biblioteca.livro_dto_response import Livro_dto_response
from .service_exception import Service_Exception

class Livro_service:
    def __init__(self, repository:Interface_Dao[Livro],
                 library_client: IBiblioteca_interface,
                 ia_client: IIa_interface):
        self.repository = repository
        self.library_client = library_client
        self.ia_client = ia_client
    

    async def insert(self,livro_schema: Livro_schema) -> int:
        try:
            livro = Livro(**livro_schema.model_dump())
            livro = await self._check_library_about(livro)

            await self.repository.insert(livro)
            return   livro.id
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
    
    async def _check_library_about(self,livro: Livro|Livro_dto_response) -> Livro:
        if not livro.sobre or not livro.sobre.strip():
            response= await self.ia_client.about_book(livro)
            livro.sobre = response.sobre
        return livro