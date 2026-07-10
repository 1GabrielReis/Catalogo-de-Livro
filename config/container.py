from .settings import Settings
from clients.api_biblioteca.biblioteca_settings import Biblioteca_settings
from clients.api_biblioteca.biblioteca_api_client import Biblioteca_api_client

from clients.api_ia.ia_settings import IA_settings
from clients.api_ia.ia_api_client import IA_api_client

from models.dao.implementation.livro_dao_mongo import Livro_dao_mongo
from database.connections.pymongo.db_mongo import DB_mongo

from service.livro_service import Livro_service

class Container:
    def __init__(self,set:Settings):
        self.set = set
        self._registros = {}
        self._instancias = {}
        self.dependencias()

    def registrar(self, interface, factory):
        self._registros[interface] = factory

    def get(self, interface):
        if interface in self._instancias:
            return self._instancias[interface]

        factory = self._registros.get(interface)
        if factory is None:
            raise Exception(f"Nada registrado para {interface}")

        instancia = factory(self)
        self._instancias[interface] = instancia
        return instancia
    
    def dependencias(self):
        s: Settings = self.set

        self.registrar("db", lambda c: DB_mongo(url_config=s.data_base_url, db_config=s.data_base))
        self.registrar("biblioteca", lambda c: Biblioteca_settings(base_url=s.biblioteca_url,username=s.blioteca_user))
        self.registrar("ia", lambda c: IA_settings(key=s.ia_key, MODEL_ID=s.model_id))
        
        self.registrar("ILivro_interface", lambda c: Livro_dao_mongo(db=c.get("db")))
        self.registrar("IBiblioteca_interface", lambda c: Biblioteca_api_client(settings=c.get("biblioteca")))
        self.registrar("IIa_interface", lambda c: IA_api_client(settings=c.get("ia")))

        self.registrar("Livro_service", lambda c: Livro_service(repository=c.get("ILivro_interface"),
                                                                ia_client=c.get("IIa_interface"),
                                                                library_client=c.get("IBiblioteca_interface")))
            

            



