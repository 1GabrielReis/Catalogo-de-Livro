#biblioteca DB
import pymongo as mongo
from pymongo import errors 

from ..db_Exception import DB_Exception
from ..db_base import DB_base

class DB_mongo(DB_base):
    def __init__(self, url_config, db_config):
        super().__init__()
        self.url_config = url_config
        self.db_config = db_config
        self.bd = None 
        self.client = None

    def _loadProperties(self):
        try:
            self.client = mongo.MongoClient(self.url_config,serverSelectionTimeoutMS=5000)
            self.client.admin.command('ping')
        except errors.ConnectionFailure as erro:
            raise DB_Exception(f'Erro: Conectação ao MongoDB\ninfo:{erro}')
        except Exception as erro:
            raise DB_Exception(f'Erro inesperado: \ninfo:{erro}')

    def getConn(self):
        if self.bd is None:
            try:
                
                self._loadProperties()
                self.bd = self.client[self.db_config]
            except errors.ServerSelectionTimeoutError as erro:
                raise DB_Exception(f'Erro: Conectação ao Data base\ninfo:{erro}')
            except Exception as erro:
                raise DB_Exception(f'Erro inesperado: \ninfo:{erro}')
        return self.bd

    def closeCursor(self, cursor): #só funciona no find, o find_one não precisa 
        if cursor is not None:
            try:
                if hasattr(cursor, 'close'):
                    cursor.close()
            except errors.OperationFailure as erro:
                raise DB_Exception(f'Erro ao fechar o cursor \ninfo:{erro}') 
            except Exception as erro:
                raise DB_Exception(f'Erro inesperado: \ninfo:{erro}')   

    def disconnect(self):
        if self.client is not None:
            try:
                self.client.close()
                self.client = None
                self.bd = None
            except errors.ConnectionFailure as erro:
                raise DB_Exception(f'Erro ao fecha conexão \ninfo:{erro}') 
            except Exception as erro:
                raise DB_Exception(f'Erro inesperado: \ninfo:{erro}')
