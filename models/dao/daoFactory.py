from .implementation.ivro_dao_mongo import Livro_dao_mongo

class DaoFactory:
    def createlivro():
        return Livro_dao_mongo()