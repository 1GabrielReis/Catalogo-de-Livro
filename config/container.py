from .settings import Settings
from models.dao.implementation.livro_dao_mongo import Livro_dao_mongo
from clients.api_biblioteca.biblioteca_api_client import Biblioteca_api_client
from clients.api_ia.ia_api_client import IA_api_client
class Container:
    def __init__(self,
                 livro_bd: Livro_dao_mongo,
                 biblioteca_api: Biblioteca_api_client,
                 ia_api: IA_api_client):
        self.livro_bd = livro_bd
        self.biblioteca_api = biblioteca_api
        self.ia_api = ia_api
        self.container = self._container_dict()

        
    def _container_dict(self) -> dict:
        return {
            "ILivro_interface":self.livro_bd,
            "IBiblioteca_interface": self.biblioteca_api,
            "IA_dto_response":self.ia_api
        }