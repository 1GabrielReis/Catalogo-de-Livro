from unittest.mock import MagicMock, patch

from models.entities.livro import Livro

# test
def test_insert(livro_dao,livro):
    mock_insert_result = MagicMock()
    mock_insert_result.inserted_id = '6a2aedeeb584d200e6d711f0'

    comando_mongo = 'pymongo.collection.Collection.insert_one'
    with patch.object(livro_dao, '_check_duplicity', return_value=""):
        with patch(comando_mongo, return_value=mock_insert_result):
            livro_dao.insert(livro)
            assert isinstance(livro.id, str)
            assert livro.id is not None
            assert livro.id == '6a2aedeeb584d200e6d711f0'
    

def test_update(livro_dao,livro):
    mock_update_result = MagicMock()
    mock_update_result.modified_count = 1

    livro.id = '6a2aedeeb584d200e6d711f0'

    comando_mongo = 'pymongo.collection.Collection.update_one'
    with patch.object(livro_dao, '_check_duplicity', return_value=""):
        with patch(comando_mongo, return_value=mock_update_result):
            resposta = livro_dao.update(livro)
            assert isinstance(resposta, bool)
            assert resposta is not None
            assert resposta is True


def test_deleteById(livro_dao):
    mock_resultado_mongo = MagicMock() 
    mock_resultado_mongo.deleted_count = 1

    id_livro = '6a2aedeeb584d200e6d711f0'

    comando = 'pymongo.collection.Collection.delete_one'
    with patch(comando,return_value = mock_resultado_mongo):
        resposta = livro_dao.deleteById(id_livro)

        print(f'Respsota: {resposta}')
        assert resposta is not None
        assert isinstance(resposta,bool)

def test_findById(livro_dao):
    id_livro = '6a2aedeeb584d200e6d711f0'
    livro = livro_dao.findById(id_livro)
    print(f"\n---test_findById---\n{livro}")
    assert livro is not None
    assert isinstance(livro,Livro) 

def test_findByTitle(livro_dao):
    titulo ='A Revolução '
    livros = livro_dao.findByTitle(titulo)
    print("\n---findByTitle---")
    for livro in livros:
        print("\n",livro)
    assert isinstance(livros,list) 

def test_findAll(livro_dao):
    livros = livro_dao.findAll()
    print("\n---test_findAll---")
    for livro in livros:
        print("\n",livro)
    assert isinstance(livros,list) 
