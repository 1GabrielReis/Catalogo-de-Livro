from ...models.entities.livro import Livro
from ...models.dao.implementation.interface_Dao import Interface_Dao

class Livro_service:
    def __init__(self, repository:Interface_Dao):
        self.repository = repository
    