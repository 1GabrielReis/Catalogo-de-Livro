from typing import List
from bson.objectid import ObjectId
from datetime import datetime

from ...entities.livro import Livro
from ..livro_interface import ILivro_interface

from database.connections.db_Exception import DB_Exception

from pymongo import errors

class Livro_dao_mongo(ILivro_interface):
    def __init__(self,db):
        super().__init__()
        self.db = db
    
    def insert(self, livro: Livro):
        colecao = None
        try:
            if not (id := self._check_duplicity(livro)):
                campos_insert = {
                "titulo": livro.titulo,
                "autor": livro.autor,
                "editora": livro.editora,
                "data_criacao": livro.data_criacao,
                "sobre": livro.sobre,
                }
                colecao = self.db.getConn()['Livros']
                id= colecao.insert_one(campos_insert).inserted_id
            livro.id = str(id)
        except errors.DuplicateKeyError as erro:
            raise DB_Exception(f'Erro ao inserir novo livro \ninfo: {erro}')
        except Exception as erro:
            raise DB_Exception(f'Erro inesperado: \ninfo:{erro}')
                

    def update(self,livro: Livro) -> bool:
        colecao = None
        try:
            if (duplicado := self._check_duplicity(livro)) and duplicado != str(livro.id):
                return False

            id_livro = ObjectId(livro.id) if isinstance(livro.id, str) else livro.id

            colecao = self.db.getConn()['Livros']

            campos_update = {
                "titulo": livro.titulo,
                "autor": livro.autor,
                "editora": livro.editora,
                "sobre": livro.sobre,
            }
            campos_update = {k: v for k, v in campos_update.items() if v is not None}
            
            resultado = colecao.update_one(
                {'_id': id_livro},
                [{
                    "$set": {"data_criacao": {"$ifNull": ["$data_criacao", datetime.today()]},
                        **campos_update}
                }]
            )
                
            if resultado.matched_count == 0:
                raise DB_Exception(f"Categoria com ID {id_livro} não encontrada")
            return True
         
        except errors.OperationFailure as erro:
            raise DB_Exception(f'Erro ao fazer update \ninfo: {erro}')
        except Exception as erro:
            raise DB_Exception(f'Erro inesperado: \ninfo:{erro}')



    def deleteById(self, id) -> bool:
        colecao = None
        try:
            livro_id = ObjectId(id)  if isinstance(id, str) else id
            colecao = self.db.getConn()['Livros']
            resultado = colecao.delete_one({"_id": livro_id})
            #if resultado.deleted_count  == 0:
                # raise DB_Exception(f"Categoria com ID {livro_id} não encontrada")
            return resultado.deleted_count  != 0 
        except errors.OperationFailure as erro:
            raise DB_Exception(f"Erro ao deletar categoria: {erro}")
        except Exception as erro:
            raise DB_Exception(f'Erro inesperado: \ninfo:{erro}')



    def findById(self, id) -> Livro:
        colecao = None
        try:
            livro_id = ObjectId(id)  if isinstance(id, str) else id
        
            colecao = self.db.getConn()['Livros']
            cursor = colecao.find_one({"_id":livro_id})
            if not cursor:
                return None
            return self._mapping_entity(cursor)

        except errors.OperationFailure as erro:
            raise DB_Exception(f'Erro ao alterar livro \ninfo: {erro}')
        except Exception as erro:
            raise DB_Exception(f'Erro inesperado: \ninfo:{erro}')
        
    
    def findByTitle(self,title: str) -> List[Livro]:
            colecao = None
            cursor = None
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
                titulo=row.get("titulo"),
                autor=row.get("autor"),
                editora=row.get("editora"),
                sobre=row.get("sobre"),
                data_criacao=row.get("data_criacao")
            )
    
    def _check_duplicity(self, livro: Livro) -> str:
        colecao = None
        try:
            titulo, autor = livro.titulo, livro.autor
        
            colecao = self.db.getConn()['Livros']
            cursor = colecao.find_one({"$and":[{"titulo": {"$regex":titulo,"$options": "i"}},
                                               {'autor':  {"$regex":autor,"$options": "i"}}]})
            return str(cursor.get("_id")) if cursor else ""
        
        except errors.OperationFailure as erro:
            raise DB_Exception(f'Erro ao verificar \ninfo: {erro}')
        except Exception as erro:
            raise DB_Exception(f'Erro inesperado: \ninfo:{erro}')
    