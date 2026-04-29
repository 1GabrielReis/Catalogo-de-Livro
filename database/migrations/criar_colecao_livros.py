from pymongo import MongoClient
from pymongo.errors import CollectionInvalid

from ..connections.db_Exception import DB_Exception

def up(db):
    try:
        if "Livros" in db.list_collection_names():
            raise DB_Exception("Coleção 'Livros' já existe")
        schema = {
            '$jsonSchema': {
                "bsonType": "object",
                "required": ["titulo", "autor"],
                "properties": {
                    "_id": {"bsonType": "objectId"},
                    "titulo": {
                        "bsonType": "string",
                        "minLength": 3,
                        "description": "Título do livro (obrigatório, mínimo 3 caracteres)"
                    },
                    "autor": {
                        "bsonType": "string",
                        "description": "Autor do livro (obrigatório)"
                    },
                    "editora": {
                        "bsonType": "string",
                        "description": "Editora do livro (opcional)"
                    },
                    "sobre": {
                        "bsonType": "string",
                        "description": "Informações sobre o livro (opcional)"
                    },
                    "descricao_ia": {
                        "bsonType": "string",
                        "description": "Descrição gerada por IA (opcional)"
                    },
                    "data_criacao": {
                        "bsonType": "date",
                        "description": "Data de criação do registro"
                    }
                }
            }
        }
        
        db.create_collection("Livros", validator=schema)
        
    except CollectionInvalid as erro:
        raise DB_Exception(f'Coleção já existe: {str(erro)}')
    except Exception as erro:
        raise DB_Exception(f"✗ Erro ao criar coleção: {str(erro)}")

def down(db):
    try:
        if "Livros" in db.list_collection_names():
            db.drop_collection("Livros")
    except Exception as erro:
        raise DB_Exception(f"✗ Erro ao remover coleção: {str(erro)}")