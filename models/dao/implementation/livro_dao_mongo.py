from typing import List
from bson.objectid import ObjectId

from ...entities.livro import Livro
from ..livro_interface import ILivro_interface

from database.connections.db_Exception import DB_Exception

from pymongo import errors

class Livro_dao_mongo(ILivro_interface):
    def __init__(self,db):
        super().__init__()
        self.db = db
    
    def insert(self, livro: Livro):
        cursor = None
        try:
            if not (id := self._check_duplicity(livro)):
                cursor = self.db.getConn()['Livros']
                id= cursor.insert_one(**livro.__dict__).inserted_id
            livro.id = str(id)
        except errors.DuplicateKeyError as erro:
            raise DB_Exception(f'Erro ao inserir novo livro \ninfo: {erro}')
        except Exception as erro:
            raise DB_Exception(f'Erro inesperado: \ninfo:{erro}')
        finally:
            self.db.closeCursor(cursor)
                

    def update(self,livro: Livro) -> bool:
        cursor = None
        try:
            id_livro = (livro_dict := livro.__dict__).pop("id")
            id_livro = ObjectId(id_livro) if isinstance(id_livro, str) else id_livro
            
            if (duplicado := self._check_duplicity(livro)) and duplicado != str(id_livro):
                return False
            
            cursor = self.db.getConn()['Livros']
            resultado = cursor.update_one({'_id': id_livro},{"$set": livro_dict})
                
            if resultado.modified_count == 0:
                raise DB_Exception(f"Categoria com ID {id_livro} não encontrada")
            return True
         
        except errors.OperationFailure as erro:
            raise DB_Exception(f'Erro ao fazer update \ninfo: {erro}')
        except Exception as erro:
            raise DB_Exception(f'Erro inesperado: \ninfo:{erro}')
        finally:
            self.db.closeCursor(cursor)


    def deleteById(self, id) -> bool:
        cursor = None
        try:
            livro_id = ObjectId(id)  if isinstance(id, str) else id
            cursor = self.db.getConn()['Livros']
            resultado = cursor.delete_one({"_id": livro_id})
            #if resultado.deleted_count  == 0:
                # raise DB_Exception(f"Categoria com ID {livro_id} não encontrada")
            return resultado.deleted_count  == 0 
        except errors.OperationFailure as erro:
            raise DB_Exception(f"Erro ao deletar categoria: {erro}")
        except Exception as erro:
            raise DB_Exception(f'Erro inesperado: \ninfo:{erro}')
        finally:
            self.db.closeCursor(cursor)


    def findById(self, id) -> Livro:
        colecao = None
        try:
            livro_id = ObjectId(id)  if isinstance(id, str) else id
        
            colecao = self.db.getConn()['Livros']
            cursor = colecao.find_one({"_id":livro_id})
            return self._mapping_entity(cursor)

        except errors.OperationFailure as erro:
            raise DB_Exception(f'Erro ao alterar livro \ninfo: {erro}')
        except Exception as erro:
            raise DB_Exception(f'Erro inesperado: \ninfo:{erro}')
    
    def findByTitle(self,title: str) -> List[Livro]:
        colecao = None
        try:
            colecao = self.db.getConn()['Livros']
            query = {"titulo": {"$regex":title,"$options": "i"}}
            
            cursor = colecao.find(query)
            livros = [self._mapping_entity(livro) for livro in list(cursor)]

            return livros
        except errors.OperationFailure as erro:
            raise DB_Exception(f'Erro ao encontrar livros\ninfo: {erro}')
        except Exception as erro:
            raise DB_Exception(f'Erro inesperado: \ninfo:{erro}')
        finally:
            self.db.closeCursor(cursor)


    def findAll(self) -> List[Livro]:
        colecao = None
        try:
            colecao = self.db.getConn()['Livros']

            cursor = colecao.find() 

            livros = [self._mapping_entity(livro) for livro in list(cursor)]
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
    
    def _check_duplicity(self, livro: Livro) -> str:
        cursor = None
        try:
            titulo, autor = livro.titulo, livro.autor
        
            cursor = self.db.getConn()['Livros']
            livro_check = cursor.find_one({"$and":[{"titulo":titulo},{'autor':autor}]})
            return str(livro_check.get("_id")) if livro_check else ""
        
        except errors.OperationFailure as erro:
            raise DB_Exception(f'Erro ao verificar \ninfo: {erro}')
        except Exception as erro:
            raise DB_Exception(f'Erro inesperado: \ninfo:{erro}')
        finally:
            self.db.closeCursor(cursor)
    