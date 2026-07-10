import pytest

import os
from dotenv import load_dotenv

from clients.api_biblioteca.biblioteca_settings import Biblioteca_settings
from clients.api_biblioteca.biblioteca_api_client import Biblioteca_api_client

from clients.api_ia.ia_settings import IA_settings
from clients.api_ia.ia_api_client import IA_api_client
from clients.api_biblioteca.livro_dto_response import Livro_dto_response

load_dotenv()

@pytest.fixture
def biblioteca_client():
    biblioteca_set = Biblioteca_settings(base_url=os.getenv('BIBLIOTECA_URL'),
                                          username= os.getenv('BIBLIOTECA_USER'))
    return Biblioteca_api_client(biblioteca_set)

@pytest.fixture
def livro_dto():
    return Livro_dto_response( id = "6a2aedeeb584d200e6d711ef",
                               titulo=  "Crime e Castigo",
                               autor = "Fiódor Dostoiévski",
                               editora = "Saraiva")
    
@pytest.fixture
def ia_client():
    ia_set = IA_settings(key= os.getenv('IA_KEY'),
                         MODEL_ID= os.getenv('MODEL_ID'))
        
    return IA_api_client(ia_set)