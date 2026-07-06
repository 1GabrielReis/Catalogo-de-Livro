from typing import List
from pydantic import BaseModel

from models.entities.livro import Livro
from schemas.livro_schema import Livro_schema
from models.dao.livro_interface import ILivro_interface
from clients.clients_interface import IBiblioteca_interface, IIa_interface
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
        

    def update(self,livro_schema: Livro_schema, id: str) -> dict:
        try:
            if not id or not id.strip():
                return dict(info='id não informado!') 

            livro = self._format_book(livro_schema)
            livro.id = id.strip()
            self._ensure_book_about(livro)
            
            check =  self.repository.update(livro)
            return dict(check=check)
        except Exception as erro:
            raise Service_Exception(f'erro update service: \ninfo: {erro}')


    def deleteById(self, id: str) -> dict:
        try:
            if not id or not id.strip():
                return dict(info='id não informado!') 
            check =  self.repository.deleteById(id)
            return dict(check=check)
        except Exception as erro:
            raise Service_Exception(f'erro deleteById service: \ninfo: {erro}')


    def findById(self, id: str|int) -> Livro | dict:
        try:
            livro = None
            id_limpo = str(id).strip()

            if not id_limpo:
                return dict(info='id não informado!') 
            
            if id_limpo.isdigit():
                livro = self.library_client.findById(int(id_limpo))
                if livro:
                    livro = self._format_book(livro)
                    self._ensure_book_about(livro)
                    self.repository.insert(livro)
            else:
                livro = self.repository.findById(id_limpo)
            return self._format_book(livro) if livro else dict(info='Livro não encontrado')
        except Exception as erro:
            raise Service_Exception(f'erro findById service: \ninfo: {erro}')

    def findByTitle(self, title: str) -> List[Livro] | dict:
        try:
            if not title or not title.strip():
                return dict(info='titulo não informado!')         
            title = self._format_str(title)
            livros = self.repository.findByTitle(title)
            if not livros:
                livros = self.library_client.findByTitle(title)
            livros = [self._format_book(livro) for livro in livros] if livros else None
            return livros if livros else dict(info='titulo não encontrado!')
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
                livro_dict_formt[chave] = self._format_str(valor) if valor else None
        
        livro_dict_formt.setdefault('id',None)
        livro_dict_formt.setdefault('sobre',None)
        livro_dict_formt.setdefault('data_criacao',None)
        return Livro(**livro_dict_formt)


    def _to_dict(self,livro_objs) -> dict:
        if isinstance(livro_objs,BaseModel):
            livro_dict= livro_objs.model_dump()
        else:
            livro_dict= livro_objs.__dict__
        return livro_dict
    
    def _format_str(self,valor:str):
        return " ".join(palavra.title() for palavra in valor.split())

