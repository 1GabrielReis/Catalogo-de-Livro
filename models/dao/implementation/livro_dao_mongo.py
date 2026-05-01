from typing import List
from datetime import date

from ...entities.livro import Livro
from ...schemas.livro_schema import Livro_schema
from .base_dao import BaseDao

from ....database.connections.db_Exception import DB_Exception

from pymongo import errors

class Livro_dao_mongo(BaseDao[Livro]):
    def __init__(self,db):
        super().__init__()
        self.db = db
    
    def insert(self, livro: Livro) -> int:
        cursor = None
        try:
            livro_schema= Livro_schema(**livro.__dict__)
            cursor = self.db.getConn()['Livros']
            id= cursor.insert_one(livro_schema.model_dump()).inserted_id
            livro.id = str(id)
        except errors.DuplicateKeyError as erro:
            raise DB_Exception(f'Erro ao inserir novo livro \ninfo: {erro}')
        except Exception as erro:
            raise DB_Exception(f'Erro inesperado: \ninfo:{erro}')
        finally:
            self.db.closeCursor(cursor)
            self.db.disconnect()
                

    def update(self,livro: Livro) -> bool:
        cursor = None
        try:
            pass
        except errors.OperationFailure:
            raise DB_Exception(f'Erro ao alterar livro \ninfo: {erro}')
        except Exception as erro:
            raise DB_Exception(f'Erro inesperado: \ninfo:{erro}')
        finally:
            self.db.closeCursor(cursor)

    def deleteById(self, id) -> bool:
        cursor = None
        try:
            pass
        except errors.OperationFailure:
            raise DB_Exception(f'Erro ao alterar livro \ninfo: {erro}')
        except Exception as erro:
            raise DB_Exception(f'Erro inesperado: \ninfo:{erro}')
        finally:
            self.db.closeCursor(cursor)

    def findById(self, id) -> Livro:
        cursor = None
        try:
            pass
        except errors.InvalidOperation:
            raise DB_Exception(f'Erro ao alterar livro \ninfo: {erro}')
        except Exception as erro:
            raise DB_Exception(f'Erro inesperado: \ninfo:{erro}')
        finally:
            self.db.closeCursor(cursor)

    def findAll(self) -> List[Livro]:
        cursor = None
        try:
            pass
        except errors.CursorNotFound:
            raise DB_Exception(f'Erro ao alterar livro \ninfo: {erro}')
        except Exception as erro:
            raise DB_Exception(f'Erro inesperado: \ninfo:{erro}')
        finally:
            self.db.closeCursor(cursor)


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