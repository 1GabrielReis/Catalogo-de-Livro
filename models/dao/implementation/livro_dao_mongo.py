from typing import List
from bson.objectid import ObjectId

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
            livro_id = ObjectId(id)  if isinstance(id, str) else id
        
            cursor = self.db.getConn()['Livros']
            livro_dict = cursor.find_one({"_id":livro_id})
            return self._mapping_entity(livro_dict)

        except errors.OperationFailure as erro:
            raise DB_Exception(f'Erro ao alterar livro \ninfo: {erro}')
        except Exception as erro:
            raise DB_Exception(f'Erro inesperado: \ninfo:{erro}')
        finally:
            self.db.closeCursor(cursor)

    def findAll(self) -> List[Livro]:
        cursor = None
        try:
            cursor = self.db.getConn()['Livros']
            livros_dict = list(cursor.find())

            livros = [self._mapping_entity(livro) for livro in livros_dict]
            return livros
        except errors.OperationFailure as erro:
            raise DB_Exception(f'Erro ao alterar livro \ninfo: {erro}')
        except Exception as erro:
            raise DB_Exception(f'Erro inesperado: \ninfo:{erro}')
        finally:
            self.db.closeCursor(cursor)


    def _mapping_entity(self, row: dict) -> Livro:
            """Mapeia uma linha do banco para a entidade Livro"""
            return Livro(
                id= str(row['_id']),
                titulo=row["titulo"],
                autor=row["autor"],
                editora=row["editora"],
                sobre=row["sobre"],
                data_criacao=row["data_criacao"]
            )