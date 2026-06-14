from typing import List, TypeVar, Generic

from models.entities.livro import Livro
from schemas.livro_schema import Livro_schema
from models.dao.livro_interface import ILivro_interface
from clients.clients_interface import IBiblioteca_interface, IIa_interface
from clients.api_biblioteca.livro_dto_response import Livro_dto_response
from .service_exception import Service_Exception

class Livro_service:
    def __init__(self, repository:ILivro_interface,
                 library_client: IBiblioteca_interface,
                 ia_client: IIa_interface):
        self.repository = repository
        self.library_client = library_client
        self.ia_client = ia_client
    

    def insert(self,livro_schema: Livro_schema) -> dict:
        try:
            livro = Livro(**self._format_book(livro_schema))
            livro = self._check_library_about(livro)

            self.repository.insert(livro)
            return  dict(id=livro.id)
            
        except Exception as erro:
            raise Service_Exception(f'erro insert service: \ninfo: {erro}')
        

    def update(self,livro_schema: Livro_schema) -> dict:
        try:
            livro = Livro(**self._format_book(livro_schema.model_dump()))
            livro = self._check_library_about(livro)
            check =  self.repository.update(livro)
            return dict(check=check)
        except Exception as erro:
            raise Service_Exception(f'erro update service: \ninfo: {erro}')


    def deleteById(self, id: str) -> dict:
        try:
            check =  self.repository.deleteById(id)
            return dict(check=check)
        except Exception as erro:
            raise Service_Exception(f'erro deleteById service: \ninfo: {erro}')


    def findById(self, id: str) -> Livro:
        try:
            livro = self.repository.findById(id)
            if not livro and id.strip().isdigit():
                livro = self.library_client.findById(int(id))
                if livro:
                    livro_dto = self.ia_client.about_book(livro)
                    livro = Livro(**self._format_book(**livro_dto))
                    self.repository.insert(livro)
            return livro
        except Exception as erro:
            raise Service_Exception(f'erro findById service: \ninfo: {erro}')

    def findByTitle(self, title: str) -> List[Livro]:
        try:
            title = " ".join([palavra.title() for palavra in title.split()])
            livros = self.repository.findByTitle(title)
            if not livros:
                livros = self.library_client.findByTitle(title)
                if livros:
                    livros = [Livro(**self._format_book(livro)) for livro in livros]
            return livros
        except Exception as erro:
            raise Service_Exception(f'erro findById service: \ninfo: {erro}')

    def findAll(self) -> List[Livro]:
        try:
            return self.repository.findAll()
        except Exception as erro:
            raise Service_Exception(f'erro findAll service: \ninfo: {erro}')
    
    def _check_library_about(self,livro: Livro|Livro_dto_response) -> Livro:
        if not livro.sobre or not livro.sobre.strip():
            response= self.ia_client.about_book(livro)
            livro.sobre = response.sobre
        return livro
        
    def _format_book(self, livro:Livro_schema|Livro_dto_response) -> dict:
        return dict(id= livro.id.strip() if livro.id else None,
                     titulo= " ".join([palavra.title() for palavra in livro.titulo.split()]),
                     autor= " ".join([nome.title() for nome in livro.autor.split()]),
                     editora= " ".join([empresa.lower() for empresa in livro.editora.split()]),
                     sobre= livro.sobre.strip() if livro.sobre else None,
                     data_criacao= livro.data_criacao)
