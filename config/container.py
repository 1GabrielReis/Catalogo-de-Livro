from .settings import Settings
from ..models.dao.implementation.livro_dao_mongo import Livro_dao_mongo
from ..clients.api_biblioteca.biblioteca_api_client import Biblioteca_api_client
from ..clients.api_ia.ia_api_client import IA_api_client
class Container:
    def __init__(self):
        self.container = self.container_set()
        
    def _container_set(self):
        return {
            "ILivro_interface":Livro_dao_mongo,
            "IBiblioteca_interface": Biblioteca_api_client,
            "IA_dto_response":IA_api_client
        }