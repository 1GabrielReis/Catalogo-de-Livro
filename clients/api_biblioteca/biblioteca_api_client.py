import httpx

from typing import List

from ..clients_interface import IBiblioteca_interface
from .biblioteca_settings import Biblioteca_settings
from .livro_dto_response import Livro_dto_response
from .biblioteca_exception import Biblioteca_exception


class Biblioteca_api_client(IBiblioteca_interface):
    def __init__(self, settings: Biblioteca_settings):
        self.settings = settings

    def findById(self,id: int) -> Livro_dto_response:
        try:
            with httpx.AsyncClient() as client:
                url = f'{self.settings.base_url}/{self.settings.username}'
                response = client.get(f'{url}/id/{id}')

                if response.status_code != 200:
                    raise Biblioteca_exception(f'Erro na requisição:{response.status_code}')
                
                data= response.json()
                return Livro_dto_response(**data['dados'])
        
        except httpx.HTTPError as erro:
            raise Biblioteca_exception(f'Erro ao tentar fazer requisção com API biblioteca \ninfo: {erro} ')
        except Exception as erro:
            raise Biblioteca_exception(f'Erro inesperado. Camda de API biblioteca \ninfo: {erro}')


    def findByTitle(self,titulo: str) -> List[Livro_dto_response]:
        try:
            with httpx.AsyncClient() as client:
                url = f'{self.settings.base_url}/{self.settings.username}'
                response = client.get(f'{url}/titulo/{titulo}')

                if response.status_code != 200:
                    raise Biblioteca_exception(f'Erro na requisição:{response.status_code}')
                
                data= response.json()
                lista_livros = data.get('dados', [])
                return [Livro_dto_response(**livro) for livro in lista_livros]
        
        except httpx.HTTPError as erro:
            raise Biblioteca_exception(f'Erro ao tentar fazer requisção com API biblioteca \ninfo: {erro} ')
        except Exception as erro:
            raise Biblioteca_exception(f'Erro inesperado. Camda de API biblioteca \ninfo: {erro}')