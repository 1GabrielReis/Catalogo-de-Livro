import os
from dotenv import load_dotenv

#biblioteca DB
import pymongo as mongo
from pymongo import errors as erro

from .db_Exception import DB_Exception
from .db_base import DB_base

class DB_mongo(DB_base):
    def __init__(self, bd=None, client=None):
        super().__init__()
        self.bd = bd
        self.client = client

    def _loadProperties(self, url):
        try:
            self.client = mongo.MongoClient(url)
        except erro.ConnectionFailure as erro:
            raise DB_Exception(f'Erro: Conectação ao MongoDB\ninfo:{erro}')
        except Exception as erro:
            raise DB_Exception(f'Erro inesperado: \ninfo:{erro}')

    def getConn(self, **kwargs):
        if self.bd is None:
            try:
                mongo_DB = kwargs['DB']
                mongo_url = kwargs['url']
                
                self._loadProperties(mongo_url)
                self.bd = self.client[mongo_DB]
                return self.bd
            except erro.ServerSelectionTimeoutError as erro:
                raise DB_Exception(f'Erro: Conectação ao Data base\ninfo:{erro}')
            except Exception as erro:
                raise DB_Exception(f'Erro inesperado: \ninfo:{erro}')

    def closeCursor(self, curso):
        if curso is not None:
            try:
                curso.close()
            except erro.OperationFailure as erro:
                raise DB_Exception(f'Erro ao fechar o curso \ninfo:{erro}') 
            except Exception as erro:
                raise DB_Exception(f'Erro inesperado: \ninfo:{erro}')   

    def disconnect(self):
        if self.bd is not None:
            try:
                self.client.close()
                self.client = None
                self.bd = None
            except erro.ConnectionFailure as erro:
                raise DB_Exception(f'Erro ao fecha conexão \ninfo:{erro}') 
            except Exception as erro:
                raise DB_Exception(f'Erro inesperado: \ninfo:{erro}')
    

