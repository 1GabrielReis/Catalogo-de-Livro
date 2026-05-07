import requests

from .biblioteca_settings import Biblioteca_settings
from .livro_dto_response import Livro_dto_response
from .biblioteca_exception import Biblioteca_exception


class biblioteca_api_client:
    def __init__(self, settings: Biblioteca_settings):
        self.settings = settings

    def findById(self,id: int) -> Livro_dto_response:
        try:
            url = f'{self.settings.base_url}/{self.settings.username}'
            response = requests.get(url=url, params={"id": id})

            if response.status_code != 200:
                raise Biblioteca_exception(f'Erro na requisição:{response.status_code}')
            
            data= response.json()
            return Livro_dto_response(**data)
        
        except requests.exceptions.RequestException as erro:
            raise Biblioteca_exception(f'Erro ao tentar fazer requisção com API biblioteca \ninfo: {erro} ')
        except Exception as erro:
            raise Biblioteca_exception(f'Erro inesperado. Camda de API biblioteca \ninfo: {erro}')


