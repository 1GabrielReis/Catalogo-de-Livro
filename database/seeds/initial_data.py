from datetime import datetime 
from pymongo.errors import DuplicateKeyError

from ..connections.db_Exception import DB_Exception
from ..connections.db_mongo import DB_mongo

def datetime_date():
    data_time = datetime.today()
    return data_time.replace(hour=0,minute=0,second=0,microsecond=0)

def up(db: DB_mongo):
    data_base = None 
    try:
        data_base = db.getConn()
        
        if "Livros" not in data_base.list_collection_names():
            raise DB_Exception("Coleção 'Livros' não existe. Execute as migrations primeiro.")
        
        livros = [
            {
                "titulo": "Crime e Castigo",
                "autor": "Fiódor Dostoiévski",
                "editora": "Saraiva",
                "sobre": "Uma obra clássica da literatura russa que explora temas de moralidade, culpa e redenção através da história de Raskólnikov.",
                "descricao_ia": None,
                "data_criacao": datetime_date()
            },
            {
                "titulo": "Orgulho e Preconceito",
                "autor": "Jane Austen",
                "editora": "Intrínseca",
                "sobre": "Romance de costumes que retrata a sociedade inglesa do século XIX através das aventuras amorosas de Elizabeth Bennet e Mr. Darcy.",
                "descricao_ia": None,
                "data_criacao": datetime_date()
            },
            {
                "titulo": "A Revolução Silenciosa",
                "autor": "Margaret Atwood",
                "editora": "Companhia das Letras",
                "sobre": "Uma narrativa contemporânea sobre mudanças sociais, resistência e a luta pelo poder em um mundo em transformação.",
                "descricao_ia": None,
                "data_criacao": datetime_date()
            }
        ]
        colecao = data_base["Livros"]
        # Insere cada livro na coleção
        resultado = colecao.insert_many(livros)
        
        if not resultado.inserted_ids:
            raise DB_Exception(f"Erro ao inserir dados iniciais")
            
    except DuplicateKeyError as erro:
        raise DB_Exception(f"Erro: ISBN duplicado ao inserir dados. {str(erro)}")


def down(db: DB_mongo):
    data_base = None 
    try:
        data_base = db.getConn()
        
        if "Livros" not in data_base.list_collection_names():
            raise DB_Exception("Coleção 'Livros' não existe.")
        
        titulos_para_remover = [
            "Crime e Castigo",
            "Orgulho e Preconceito",
            "A Revolução Silenciosa"
        ]
        
        colecao = data_base["Livros"]
        for titulo in titulos_para_remover:
            colecao.delete_one({"titulo": titulo})
            
    except Exception as erro:
        raise DB_Exception(f"Erro ao remover dados: {str(erro)}")
    