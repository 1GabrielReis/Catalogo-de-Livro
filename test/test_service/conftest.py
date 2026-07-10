
import pytest
from pydantic import BaseModel
from datetime import date

import os
from dotenv import load_dotenv
from unittest.mock import MagicMock, patch
from random import randint as rad

from service.livro_service import Livro_service
from clients.api_biblioteca.biblioteca_settings import Biblioteca_settings
from clients.api_biblioteca.biblioteca_api_client import Biblioteca_api_client
from clients.api_ia.ia_settings import IA_settings
from clients.api_ia.ia_api_client import IA_api_client
from database.connections.pymongo.db_mongo import DB_mongo
from models.dao.implementation.livro_dao_mongo import Livro_dao_mongo

from models.entities.livro import Livro
from clients.api_biblioteca.livro_dto_response import Livro_dto_response
from clients.api_ia.ia_dto_response import IA_dto_response

# sem plugins porque você tera que colocar __init__.py em todos os arquivos :(
#pytest_plugins = ["test.test_clients.conftest","test.test_implementation_dao.conftest"]

load_dotenv()

@pytest.fixture
def biblioteca_client():
    biblioteca_set = Biblioteca_settings(base_url=os.getenv('BIBLIOTECA_URL'),
                                          username= os.getenv('BIBLIOTECA_USER'))
    return Biblioteca_api_client(biblioteca_set)

@pytest.fixture
def ia_client():
    ia_set = IA_settings(key= os.getenv('IA_KEY'),
                         MODEL_ID= os.getenv('MODEL_ID'))      
    return IA_api_client(ia_set)

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

#----- service -----
@pytest.fixture
def service(livro_dao, biblioteca_client, ia_client):
    return  Livro_service(
        repository= livro_dao,
        library_client= biblioteca_client,
        ia_client= ia_client
    )

#----- dados -----
@pytest.fixture
def livros():
    return  [
                Livro(
                    id="6a2aedeeb584d200e6d711ef",
                    titulo="Crime e Castigo",
                    autor="Fiódor Dostoiévski",
                    editora="Saraiva",
                    sobre="Uma obra clássica da literatura russa que explora temas de moralidade, culpa e redenção através da história de Raskólnikov.",
                    data_criacao=date(2026, 6, 11)
                ),
                Livro(
                    id="6a2aedeeb584d200e6d711f0",
                    titulo="Orgulho e Preconceito",
                    autor="Jane Austen",
                    editora="Intrínseca",
                    sobre="Romance de costumes que retrata a sociedade inglesa do século XIX através das aventuras amorosas de Elizabeth Bennet e Mr. Darcy.",
                    data_criacao=date(2026, 6, 11)
                ),
                Livro(
                    id="6a2aedeeb584d200e6d711f1",
                    titulo="A Revolução Silenciosa",
                    autor="Margaret Atwood",
                    editora="Companhia das Letras",
                    sobre="Uma narrativa contemporânea sobre mudanças sociais, resistência e a luta pelo poder em um mundo em transformação.",
                    data_criacao=date(2026, 6, 11)
                )
        ]

@pytest.fixture
def biblioteca():
    return {
            "status": "sucesso",
            "quantidade": 21,
            "dados": [
                {
                "id": 1,
                "titulo": "O Alquimista",
                "autor": "Paulo Coelho",
                "editora": "Rocco"
                },
                {
                "id": 2,
                "titulo": "Dom Casmurro",
                "autor": "Machado de Assis",
                "editora": "Editora Nacional"
                },
                {
                "id": 3,
                "titulo": "1984",
                "autor": "George Orwell",
                "editora": "Companhia das Letras"
                },
                {
                "id": 4,
                "titulo": "A Moreninha",
                "autor": "Joaquim Manuel de Macedo",
                "editora": "Saraiva"
                },
                {
                "id": 5,
                "titulo": "O Primo Basílio",
                "autor": "José de Alencar",
                "editora": "Editora Brasileira"
                }
            ]
        }

# ----- fixture principal -----
@pytest.fixture
def service_insert(livro_dao, insert_fake, format_book):
    patch_duplicidade = patch.object(livro_dao, '_check_duplicity', return_value="")
    patch_mongo = patch('pymongo.collection.Collection.insert_one')
    patch_ia = patch("clients.api_ia.ia_settings.genai.Client")

    patch_duplicidade.start()
    mock_insert = patch_mongo.start()
    mock_ia_class = patch_ia.start()

    mock_genai_instance = MagicMock()
    mock_ia_class.return_value = mock_genai_instance

    def _execute_cenario(livro_schema):
        livro_esperado = format_book(livro_schema)
        
        if not livro_esperado.sobre or not livro_esperado.sobre.strip():
            texto_ia_customizado = f"Resumo Inteligente: O livro {livro_esperado.titulo} aborda temas profundos..."
            
            mock_response = MagicMock()
            mock_response.text = texto_ia_customizado
            mock_genai_instance.models.generate_content.return_value = mock_response
            
            livro_esperado.sobre = texto_ia_customizado

        id_fake = insert_fake()
        livro_esperado.id = id_fake
        
        mock_result = MagicMock()
        mock_result.inserted_id = id_fake
        mock_insert.return_value = mock_result

        return livro_esperado
    
    yield _execute_cenario

    patch_ia.stop()
    patch_mongo.stop()
    patch_duplicidade.stop()


@pytest.fixture
def service_update(livro_dao, format_book, livros):
    patch_duplicidade = patch.object(livro_dao, '_check_duplicity', return_value="")
    patch_mongo = patch('pymongo.collection.Collection.update_one')
    patch_ia = patch("clients.api_ia.ia_settings.genai.Client")

    patch_duplicidade.start()
    mock_update = patch_mongo.start()
    mock_ia_class = patch_ia.start()

    mock_genai_instance = MagicMock()
    mock_ia_class.return_value = mock_genai_instance

    def _execute_cenario(livro_schema,id:str):
        livro_esperado = format_book(livro_schema)
        livro_esperado.id= id.strip()

        if not livro_esperado.sobre or not livro_esperado.sobre.strip():
            texto_ia_customizado = f"Resumo Inteligente: O livro {livro_esperado.titulo} aborda temas profundos..."
            
            mock_response = MagicMock()
            mock_response.text = texto_ia_customizado
            mock_genai_instance.models.generate_content.return_value = mock_response
            
            livro_esperado.sobre = texto_ia_customizado

        livro_encontrado = False
        for livro in livros:
            if livro.id == livro_esperado.id:
                livro_encontrado = True
                livro.titulo = livro_esperado.titulo if livro_esperado.titulo else livro.titulo
                livro.autor = livro_esperado.autor if livro_esperado.autor else livro.autor
                livro.editora = livro_esperado.editora if livro_esperado.editora else livro.editora
                livro.sobre = livro_esperado.sobre 
                if livro_esperado.data_criacao:
                    livro.data_criacao = livro_esperado.data_criacao
                break

        mock_result = MagicMock()
        mock_result.modified_count = 1 if livro_encontrado else 0
        mock_result.matched_count = 1 if livro_encontrado else 0
        mock_update.return_value = mock_result

        return livros
    
    yield _execute_cenario

    patch_ia.stop()
    patch_mongo.stop()
    patch_duplicidade.stop()

@pytest.fixture
def service_delete(livros):
    patch_mongo = patch('pymongo.collection.Collection.delete_one')

    mock_delete = patch_mongo.start()

    def _execute_cenario(id):

        livro_encontrado = False
        for livro in livros:
            livro_encontrado = True
            if livro.id == id:
                livros.remove(livro)
                break

        mock_result = MagicMock()
        mock_result.deleted_count = 1 if livro_encontrado else 0
        mock_delete.return_value = mock_result

        return livros

    yield _execute_cenario
    patch_mongo.stop()

@pytest.fixture
def service_findById(livro_dao, format_book, livros, biblioteca, insert_fake):
    patch_duplicidade = patch.object(livro_dao, '_check_duplicity', return_value="")
    patch_mongo_find = patch('pymongo.collection.Collection.find_one')
    patch_mongo_insert = patch('pymongo.collection.Collection.insert_one')
    
    patch_ia = patch("clients.api_ia.ia_settings.genai.Client")
    patch_client = patch("httpx.Client")

    patch_duplicidade.start()
    mock_find = patch_mongo_find.start()
    mock_insert = patch_mongo_insert.start()
    mock_ia_class = patch_ia.start()
    mock_client_class = patch_client.start()

    mock_genai_instance = MagicMock()
    mock_ia_class.return_value = mock_genai_instance

    mock_instancia_http = MagicMock()
    mock_response_http = MagicMock()
    
    mock_client_class.return_value.__enter__.return_value = mock_instancia_http
    mock_instancia_http.get.return_value = mock_response_http

    def _execute_cenario(id_busca):
        id_fake_gerado = None
        livro_dict_retorno = None
        banco_dict = None

        if not str(id_busca).isdigit():
            id_form = str(id_busca).strip()

            for livro_obj in livros:
                if id_form == livro_obj.id:
                    livro_dict = _to_dict(livro_obj)
                    if 'id' in livro_dict and '_id' not in livro_dict:
                        livro_dict['_id'] = livro_dict.pop('id')

                    banco_dict = livro_dict
                    break

            mock_find.return_value = banco_dict
        
        else:
            id_busca_int = int(id_busca)
            
            for lib_dict in biblioteca['dados']:
                if id_busca_int == lib_dict['id']:
                    resultado_entidade = format_book(lib_dict)

                    if not resultado_entidade.sobre or not resultado_entidade.sobre.strip():
                        texto_ia_customizado = f"Resumo Inteligente: O livro {resultado_entidade.titulo} aborda temas profundos..."
                        resultado_entidade.sobre = texto_ia_customizado

                        mock_response_ia = MagicMock()
                        mock_response_ia.text = texto_ia_customizado
                        mock_genai_instance.models.generate_content.return_value = mock_response_ia

                    id_original_api = str(resultado_entidade.id)
                    
                    id_fake_gerado = insert_fake()
                    
                    mock_result_mongo = MagicMock()
                    mock_result_mongo.inserted_id = id_fake_gerado
                    mock_insert.return_value = mock_result_mongo

                    resultado_entidade.id = id_original_api
                    livro_dict_retorno = _to_dict(resultado_entidade)
                    
                    mock_response_http.status_code = 200
                    mock_response_http.json.return_value = {
                        "status": "sucesso",
                        "dados": lib_dict
                    }
                    break

        return {
            "status": "sucesso",
            "dados": livro_dict_retorno if livro_dict_retorno else banco_dict,
            "novo_registro(_id)": id_fake_gerado
        }
    
    yield _execute_cenario

    patch_client.stop()
    patch_ia.stop()
    patch_mongo_insert.stop()
    patch_mongo_find.stop()
    patch_duplicidade.stop()
              

@pytest.fixture
def service_findByTitle(format_book, livros,biblioteca):
    patch_mongo = patch('pymongo.collection.Collection.find')
    patch_client = patch("clients.api_biblioteca.biblioteca_api_client.httpx.Client")

    mock_find = patch_mongo.start()
    mock_client_class = patch_client.start()

    mock_instancia_http = MagicMock()
    mock_response_http = MagicMock()
    mock_client_class.return_value.__enter__.return_value = mock_instancia_http

    def _execute_cenario(titulo_busca):
            titulo_form = _format_str(titulo_busca)
            
            lista_banco_dict = [] 
            lista_resultado_teste = [] 

            for livro_obj in livros:
                if titulo_form.lower() in _format_str(livro_obj.titulo).lower():
                    livro_dict = _to_dict(livro_obj)
                    if 'id' in livro_dict and '_id' not in livro_dict:
                        livro_dict['_id'] = livro_dict.pop('id')
                    
                    lista_banco_dict.append(livro_dict)
                    lista_resultado_teste.append(livro_obj)

            mock_find.return_value = lista_banco_dict

            if not lista_banco_dict:
                lista_api_json = []
            
                for lib_dict in biblioteca['dados']:
                    if titulo_form.lower() in _format_str(lib_dict['titulo']).lower():
                        lista_api_json.append(lib_dict)
                        
                        livro_formatado_api = format_book(lib_dict)
                        lista_resultado_teste.append(livro_formatado_api)
                
                mock_response_http.status_code = 200
                mock_response_http.json.return_value = {
                    "status": "sucesso",
                    "quantidade": len(lista_api_json),
                    "dados": lista_api_json
                }
                mock_instancia_http.get.return_value = mock_response_http

            return lista_resultado_teste
    
    yield _execute_cenario
    
    patch_client.stop()
    patch_mongo.stop()

        
@pytest.fixture
def service_findAll(livros):
    patch_mongo_find = patch('pymongo.collection.Collection.find')
    mock_find = patch_mongo_find.start()
    
    def _execute_cenario():
        lista_dicts_banco = []
        
        for livro_obj in livros:
            livro_dict = _to_dict(livro_obj)
            
            if 'id' in livro_dict:
                livro_dict['_id'] = livro_dict.pop('id')
                
            lista_dicts_banco.append(livro_dict)
        
        mock_find.return_value = lista_dicts_banco
        
        return livros

    yield _execute_cenario

    patch_mongo_find.stop()


# ----- fixture auxiliares -----

@pytest.fixture
def format_book():
    def _formatar(livro_objs: object) -> Livro:
        livro_dict = _to_dict(livro_objs)
        livro_dict_formt = dict()

        for chave, valor in livro_dict.items():
            if chave in ("id", "sobre"):
                livro_dict_formt[chave] = str(valor).strip() if valor else None
            elif chave == "data_criacao":
                livro_dict_formt[chave] = valor 
            else:
                livro_dict_formt[chave] = _format_str(valor) if valor else None
        
        livro_dict_formt.setdefault('id', None)
        livro_dict_formt.setdefault('sobre', None)
        livro_dict_formt.setdefault('data_criacao', None)
        return Livro(**livro_dict_formt)
    return _formatar


def _to_dict(livro_objs) -> dict:
    if isinstance(livro_objs, dict):
        return livro_objs
    elif isinstance(livro_objs, BaseModel):
        return livro_objs.model_dump()
    return getattr(livro_objs, "__dict__", {})

def _format_str(valor:str):
    return " ".join(palavra.title() for palavra in valor.split())

@pytest.fixture
def biblioteca_check(biblioteca):

    def _localizar(id_or_title) -> dict:
        livros=biblioteca['dados']
        lista= list()
        for livro in livros:
            if isinstance(id_or_title,int):
                if livro['id'] == id_or_title:
                    return {"status": "sucesso","dados":livro}
            else:
                if str(id_or_title).lower() in livro['titulo'].lower():
                    lista.append(livro)
        return {"status": "sucesso","quantidade": len(lista),"dados":lista}
    
    return _localizar

@pytest.fixture
def insert_fake():
    def _gerar_id():
        id = []
        lista_letra = ['a','b','c','d','e','f']
        while len(id) < 24:
            escolha = rad(0, 9)
            if escolha % 2 == 0:
                id.append(str(rad(0, 9)))
            else:
                id.append(lista_letra[rad(0, 5)])
        return "".join(id)
    return _gerar_id

@pytest.fixture
def livro_check(livros):

    def _localizar(id_alvo):
        for livro_dict in livros:
            if livro_dict['_id'] == id_alvo:
                return livro_dict
        return None
    
    return _localizar