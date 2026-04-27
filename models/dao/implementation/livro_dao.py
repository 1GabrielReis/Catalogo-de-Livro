from ...entities import Livro
from .base_dao import BaseDao

from typing import List

class Livro_dao(BaseDao[Livro]):
    
    def insert(self, livro: Livro) -> int:
        pass

    def update(self,livro: Livro) -> bool:
        pass

    def deleteById(self, id) -> bool:
        pass

    def findById(self, id) -> Livro:
        pass

    def findAll(self) -> List[Livro]:
        pass


    def _mapping_entity(self, row) -> Livro:
        """Mapeia uma linha do banco para a entidade Livro"""
        return Livro(
            id=row[0],
            titulo=row[1],
            autor=row[2],
            isbn=row[3],
            descricao=row[4],
            descricao_ia=row[5],
            data_criacao=row[6],
            data_atualizacao=row[7]
        )