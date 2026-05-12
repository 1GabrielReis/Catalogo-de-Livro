from pymongo.errors import OperationFailure
 
from ..connections.db_Exception import DB_Exception

def up(db):
    try:
        colecao = db['Livros']

        if 'Livros' not in db.list_collection_names():
            raise DB_Exception("Coleção 'Livros' não existe. Execute a migration anterior primeiro.")
        
        #"_id" mongo criação automaticamente 
        colecao.create_index('titulo')
        colecao.create_index('autor')
        colecao.create_index('editora')
        colecao.create_index("data_criacao")
        colecao.create_index([('titulo',1),('autor',-1)],unique=True)
    
    except OperationFailure as erro:
        raise DB_Exception(f"Erro de operação ao criar índices: {str(erro)}")
    except Exception as erro:
        raise DB_Exception(f"Erro inesperado ao criar índices: {str(erro)}")
    
def down(db):
    try:
        colecao = db["Livros"]
        
        if "Livros" not in db.list_collection_names():
            raise DB_Exception("Coleção 'Livros' não existe. Execute a migration anterior primeiro.")
        
        colecao.drop_index("titulo_1") # o mongo cria o _1 para refereir ao ordem.
        colecao.drop_index("autor_1") # sendo 1 crescente ou -1 decrescente)       
        colecao.drop_index("editora_1")
        colecao.drop_index("data_criacao_1")
        colecao.drop_index("titulo_1_autor_-1")  # Índice composto
    except OperationFailure as erro:
        raise DB_Exception(f"⚠ Índice não existe ou erro ao remover: {str(erro)}")
    except Exception as erro:
        raise DB_Exception(f"✗ Erro ao remover índices: {str(erro)}")

        
        