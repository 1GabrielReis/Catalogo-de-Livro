from typing import List, TypeVar, Generic
from pydantic import BaseModel

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
            livro = self._format_book(livro_schema)
            self._ensure_book_about(livro)

            self.repository.insert(livro)
            return  dict(id=livro.id)        
        except Exception as erro:
            raise Service_Exception(f'erro insert service: \ninfo: {erro}')
        

    def update(self,livro_schema: Livro_schema) -> dict:
        try:
            livro = self._format_book(livro_schema)
            self._ensure_book_about(livro)
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


    def findById(self, id: str) -> Livro | dict:
        try:
            livro = self.repository.findById(id)
            if not livro and id.strip().isdigit():
                livro = self.library_client.findById(int(id))
                if livro:
                    livro = self._format_book(livro)
                    self._ensure_book_about(livro)
                    self.repository.insert(livro)
            return self._format_book(livro) if livro else dict(info='Livro não encontrado')
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
            livros =  self.repository.findAll()
            return [self._format_book(livro) for livro in livros]
        except Exception as erro:
            raise Service_Exception(f'erro findAll service: \ninfo: {erro}')
    
    def _ensure_book_about(self,livro: Livro):
        if not livro.sobre or not livro.sobre.strip():
            response= self.ia_client.about_book(livro)
            livro.sobre = response.sobre
        
    def _format_book(self, livro_objs: object) -> Livro:
        livro_dict = self._to_dict(livro_objs)
        livro_dict_formt = dict()

        for chave, valor in livro_dict.items():
            if chave in ("id", "sobre"):
                livro_dict_formt[chave] = valor.strip() if valor else None
            elif chave == "data_criacao":
                livro_dict_formt[chave] = valor 
            else:
                livro_dict_formt[chave] = " ".join(palavra.title() for palavra in valor.split()) if valor else None

        return Livro(**livro_dict_formt)


    def _to_dict(self,livro_objs) -> dict:
        if isinstance(livro_objs,BaseModel):
            livro_dict= livro_objs.model_dump()
        else:
            livro_dict= livro_objs.__dict__
        return livro_dict
    
    def _format_str(self,valor:str):
        return " ".join(palavra.title() for palavra in valor.split())

