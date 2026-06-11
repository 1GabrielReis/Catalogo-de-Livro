from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import errors 

from ..db_base import DB_base
from ..db_Exception import DB_Exception

class DB_mongo(DB_base):
    def __init__(self, url_config, db_config):
        self.url_config = url_config
        self.db_config = db_config
        self.db = None 
        self.client = None

    async def _loadProperties(self):
        try:
            self.client = AsyncIOMotorClient(self.url_config)
            await self.client.admin.command('ping')
        except errors.ServerSelectionTimeoutError as erro:
            raise DB_Exception(f"Não foi possível conectar ao banco de dados! \ninfo: {erro}")
        except Exception as erro:
            raise DB_Exception(f"Erro inesperado: \ninfo: {erro}")
        
    async def getConn(self):
        try:
            if self.db:
                await self._loadProperties()
                self.db = self.client[self.db_config]
                
            return self.db
        except errors.ServerSelectionTimeoutError as erro:
            raise DB_Exception(f"Não foi possível conectar ao banco de dados! \ninfo: {erro}")
        except Exception as erro:
            raise DB_Exception(f"Erro inesperado: \ninfo: {erro}")

    def closeCursor(self):
        pass #Não precisa 

    def disconnect(self):
        try:
            self.client.close()
            self.client = None
            self.bd = None
        except errors.ServerSelectionTimeoutError as erro:
            raise DB_Exception(f"Não foi possível desconectar ao banco de dados! \ninfo: {erro}")
        except Exception as erro:
            raise DB_Exception(f"Erro inesperado: \ninfo: {erro}")