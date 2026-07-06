from view.view_entities.livro_view import Livro_view
from schemas.livro_schema import Livro_schema
from service.livro_service import Livro_service
from .controller_Exception import Controller_Exception

class Livro_controller():
    def __init__(self, service:Livro_service, view:Livro_view):
        self.service = service
        self.view = view

    def insert(self,livro_schema: Livro_schema) -> dict:
        try:
            id = self.service.insert(livro_schema)
            return self.view.info(id)   
        except Exception as erro:
            raise Controller_Exception(f'erro insert controller: \ninfo: {erro}')
        

    def update(self,id:str,livro_schema: Livro_schema) -> dict:
        try:
            check = self.service.update(id,livro_schema)
            return self.view.info(check)
        except Exception as erro:
            raise Controller_Exception(f'erro update controller: \ninfo: {erro}')


    def deleteById(self, id: str) -> dict:
        try:
            check = self.service.deleteById(id)
            return self.view.info(check)
        except Exception as erro:
            raise Controller_Exception(f'erro deleteById controller: \ninfo: {erro}')


    def findById(self, id: str) -> dict:
        try:
            livro = self.service.findById(id)
            return self.view.format(livro)
        except Exception as erro:
            raise Controller_Exception(f'erro findById controller: \ninfo: {erro}')

    def findByTitle(self, title: str) -> dict:
        try:
            livros = self.service.findByTitle(title)
            return self.view.format_list(livros)
        except Exception as erro:
            raise Controller_Exception(f'erro findById controller: \ninfo: {erro}')

    def findAll(self) -> dict:
        try:
            livros = self.service.findAll()
            return self.view.format_list(livros)
        except Exception as erro:
            raise Controller_Exception(f'erro findAll controller: \ninfo: {erro}')


    
    
