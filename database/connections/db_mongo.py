import os
from dotenv import load_dotenv

#biblioteca DB
import pymongo as mongo

from .db_Exception import DB_Exception

class DB_mongo:
    conn = None
    load_dotenv()

    @staticmethod
    def _loadProperties(url):
        if DB_mongo.conn is None:
            try:
                DB_mongo.conn = mongo.MongoClient(url)
                return DB_mongo.conn
            
            except mongo.errors.ConnectionFailure as erro:
                raise DB_Exception(f'Erro: Conectação ao MongoDB\ninfo:{erro}')
            except Exception as erro:
                raise DB_Exception(f'Erro inesperado: \ninfo:{erro}')

    @staticmethod
    def getConn(**kwargs):
        if DB_mongo.conn is None:
            try:
                mongo_DB = kwargs['DB']
                mongo_url = kwargs['url']
                
                DB_mongo._loadProperties(mongo_url)
                DB_mongo.db = DB_mongo.conn[mongo_DB]
                
                return DB_mongo.db
            
            except mongo.errors.ServerSelectionTimeoutError as erro:
                raise DB_Exception(f'Erro: Conectação ao Data base\ninfo:{erro}')
            except Exception as erro:
                raise DB_Exception(f'Erro inesperado: \ninfo:{erro}')

    @staticmethod
    def closeCursor(curso):
        if curso is not None:
            try:
                curso.close()
            except Exception.errors.OperationFailure as erro:
                raise DB_Exception(f'Erro ao fechar o curso \ninfo:{erro}') 
            except Exception as erro:
                raise DB_Exception(f'Erro inesperado: \ninfo:{erro}')   

    @staticmethod
    def disconnect():
        if DB_mongo.conn is not None:
            try:

                DB_mongo.conn.close()
                DB_mongo.conn = None
            except Exception.errors.ConnectionFailure as erro:
                raise DB_Exception(f'Erro ao fecha conexão com banco \ninfo:{erro}') 
            except Exception as erro:
                raise DB_Exception(f'Erro inesperado: \ninfo:{erro}')

