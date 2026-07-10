import pytest

import os 
from dotenv import load_dotenv
from datetime import datetime

from database.connections.pymongo.db_mongo import DB_mongo
from models.dao.implementation.livro_dao_mongo import Livro_dao_mongo
from models.entities.livro import Livro

load_dotenv()

@pytest.fixture
def db():
    conexao_mongo = DB_mongo(
        url_config= os.getenv('DATABASE_URL'),
        db_config=os.getenv('DATABASE')
    )
    yield conexao_mongo
    conexao_mongo.disconnect()

@pytest.fixture
def livro_dao(db):
    return Livro_dao_mongo(db)

@pytest.fixture
def livro():
    return Livro(id=None,
                  titulo="Crime e Castigo",
                  autor="Fiódor Dostoiévski",
                  editora="Saraiva",
                  sobre="Uma obra clássica da literatura russa que explora temas de moralidade,…",
                  data_criacao= datetime.today()
                  )
