import httpx

from typing import List

from ..clients_interface import IBiblioteca_interface
from .biblioteca_settings import Biblioteca_settings
from .livro_dto_response import Livro_dto_response
from .biblioteca_exception import Biblioteca_exception


class Biblioteca_api_client(IBiblioteca_interface):
    def __init__(self, settings: Biblioteca_settings):
        self.settings = settings
        self.timeout = httpx.Timeout(connect=5.0, read=10.0, write=5.0, pool=5.0)

    def findById(self,id: int) -> Livro_dto_response:
        try:
            with httpx.Client(timeout=self.timeout) as client:
                url = f'{self.settings.base_url}/{self.settings.username}'
                
                response = client.get(f'{url}/id/{id}')
                response.raise_for_status()
                
                data= response.json()
                return self._formt_dados(data['dados'])
            
        except httpx.TimeoutException as erro:
            raise Biblioteca_exception(f"Tempo limite ao consultar biblioteca externa: {erro}")
        except httpx.HTTPError as erro:
            raise Biblioteca_exception(f'Erro ao tentar fazer requisção com API biblioteca \ninfo: {erro} ')
        except Exception as erro:
            raise Biblioteca_exception(f'Erro inesperado. Camda de API biblioteca \ninfo: {erro}')


    def findByTitle(self,titulo: str) -> List[Livro_dto_response]:
        try:
            with httpx.Client(timeout=self.timeout) as client:
                url = f'{self.settings.base_url}/{self.settings.username}'

                response = client.get(f'{url}/titulo/{titulo}')
                response.raise_for_status()
                
                data= response.json()
                lista_livros = data.get('dados', [])
                return [self._formt_dados(livro) for livro in lista_livros]
        except httpx.TimeoutException as erro:
            raise Biblioteca_exception(f"Tempo limite ao consultar biblioteca externa: {erro}")
        except httpx.HTTPError as erro:
            raise Biblioteca_exception(f'Erro ao tentar fazer requisção com API biblioteca \ninfo: {erro} ')
        except Exception as erro:
            raise Biblioteca_exception(f'Erro inesperado. Camda de API biblioteca \ninfo: {erro}')
        

    def _formt_dados(self,dados:dict|None) -> Livro_dto_response | None:
        livro = None
        if dados:
            dados['id'] = str(dados['id'])
            livro = Livro_dto_response(**dados)
        return livro

            