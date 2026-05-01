from typing import List
from datetime import date

from ...entities.livro import Livro
from ...schemas.livro_schema import Livro_schema
from .base_dao import BaseDao

from ....database.connections.db_Exception import DB_Exception
from ....database.connections.db_mongo import DB_mongo

from pymongo import errors

class Livro_dao_mongo(BaseDao[Livro]):
    def __init__(self,db):
        super().__init__()
        self.db = db
    
    def insert(self, livro: Livro) -> int:
        cursor = None
        try:
            livro_schema= Livro_schema(**livro.__dict__)

            cursor= self.db['Livros']
            livro.id = cursor.insert_one(livro_schema.model_dump()).inserted_id

        except errors.DuplicateKeyError as erro:
            raise DB_Exception(f'Erro ao inserir novo livro \ninfo: {erro}')
        except Exception as erro:
            raise DB_Exception(f'Erro inesperado: \ninfo:{erro}')
        finally:
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