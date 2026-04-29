from datetime import date
from pymongo.errors import DuplicateKeyError

from ..connections.db_Exception import DB_Exception


def up(db):
    try:
        colecao = db["Livros"]
        
        if "Livros" not in db.list_collection_names():
            raise DB_Exception("Coleção 'Livros' não existe. Execute as migrations primeiro.")
        
        livros = [
            {
                "titulo": "Crime e Castigo",
                "autor": "Fiódor Dostoiévski",
                "editora": "Saraiva",
                "sobre": "Uma obra clássica da literatura russa que explora temas de moralidade, culpa e redenção através da história de Raskólnikov.",
                "descricao_ia": None,
                "data_criacao": date.today()
            },
            {
                "titulo": "Orgulho e Preconceito",
                "autor": "Jane Austen",
                "editora": "Intrínseca",
                "sobre": "Romance de costumes que retrata a sociedade inglesa do século XIX através das aventuras amorosas de Elizabeth Bennet e Mr. Darcy.",
                "descricao_ia": None,
                "data_criacao": date.today()
            },
            {
                "titulo": "A Revolução Silenciosa",
                "autor": "Margaret Atwood",
                "editora": "Companhia das Letras",
                "sobre": "Uma narrativa contemporânea sobre mudanças sociais, resistência e a luta pelo poder em um mundo em transformação.",
                "descricao_ia": None,
                "data_criacao": date.today()
            }
        ]
        
        # Insere cada livro na coleção
        resultado = colecao.insert_many(livros)
        
        if resultado.inserted_ids:
            quantidade = len(resultado.inserted_ids)
        else:
            quantidade = 0
            
    except DuplicateKeyError as erro:
        raise DB_Exception(f"Erro: ISBN duplicado ao inserir dados. {str(erro)}")
    except Exception as erro:
        raise DB_Exception(f"Erro ao inserir dados iniciais: {str(erro)}")


def down(db):
    try:
        colecao = db["Livros"]
        
        if "Livros" not in db.list_collection_names():
            raise DB_Exception("Coleção 'Livros' não existe.")
        
        titulos_para_remover = [
            "Crime e Castigo",
            "Orgulho e Preconceito",
            "A Revolução Silenciosa"
        ]
        
        for titulo in titulos_para_remover:
            colecao.delete_one({"titulo": titulo})
            
    except Exception as erro:
        raise DB_Exception(f"Erro ao remover dados: {str(erro)}")