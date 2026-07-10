
import pytest

import sys
import os
from unittest.mock import MagicMock, patch

from models.entities.livro import Livro
from schemas.livro_schema import Livro_schema

sys.path.append(os.path.abspath(os.path.dirname(__file__)))


#akeboshi
def test_insert(service,service_insert):
    service.ia_client.settings.client = None

    livro_entrada = Livro_schema(
        id= None,
        titulo= "drácula",
        autor= "Bram Stoker",
        editora= "Penguin Classics",
        sobre= None
    )

    livro_esperado = service_insert(livro_entrada)
    resultado = service.insert(livro_entrada)

    print("\n--- DADOS DO CENÁRIO MOCKADO ---")
    print("ID gerado pela fixture:", livro_esperado.id)
    print("Sobre gerado pela IA na fixture:", livro_esperado.sobre)
    print("Retorno real do Service:", resultado)
    print("obj livro: ",livro_esperado)

    assert resultado is not None
    assert resultado['id'] == livro_esperado.id



def test_update(service,service_update):
    service.ia_client.settings.client = None
    
    livro_alterado = Livro_schema(
        titulo= "Drácula",
        autor= "Bram Stoker",
        editora= "Penguin Classics",
        sobre= None
    )

    lista_livros_apos_update = service_update(livro_schema=livro_alterado,id= "6a2aedeeb584d200e6d711ef")
    resultado = service.update(livro_schema=livro_alterado,id= "6a2aedeeb584d200e6d711ef")

    print("\n--- RETORNO DO SERVICE ---")
    print(resultado)
    
    print("\n--- ESTADO DA LISTA DE LIVROS APÓS O UPDATE ---")
    for livro in lista_livros_apos_update:
        print(f"ID: {livro.id} | Título: {livro.titulo} | Sobre: {livro.sobre}...")

    assert resultado is not None
    livro_no_banco = next(l for l in lista_livros_apos_update if l.id == "6a2aedeeb584d200e6d711ef")
    assert livro_no_banco.titulo == "Drácula"
    assert "Resumo Inteligente" in livro_no_banco.sobre  


def test_deleteById(service,service_delete):
    id_para_deletar = "6a2aedeeb584d200e6d711ef"

    lista_apos_deletar = service_delete(id_para_deletar)
    resultado = service.deleteById(id_para_deletar)

    print("\n--- RETORNO DO SERVICE DE DELETE ---")
    print("Resultado:", resultado)

    print("\n--- LISTA DE LIVROS RESTANTES ---")
    for livro in lista_apos_deletar:
        print(f"ID: {livro.id} | Título: {livro.titulo}")

    assert resultado is not None
    assert len(lista_apos_deletar) == 2 
    assert not any(l.id == id_para_deletar for l in lista_apos_deletar)


def test_findById_DB(service, service_findById):
    id_banco = "6a2aedeeb584d200e6d711ef" 
    
    cenario = service_findById(id_banco)
    resultado_service = service.findById(id_banco)
    
    print("\n--- BUSCA NO BANCO ---")
    print("Dados simulados na fixture:", cenario["dados"])
    print("Resultado real do Service:", resultado_service)
    
    assert resultado_service is not None
    assert cenario["novo_registro(_id)"] is None 


def test_findById_Api(service, service_findById):
    service.ia_client.settings.client = None
    id_api = 3 
    
    cenario = service_findById(id_api)
    resultado_service = service.findById(id_api)
    
    print("\n--- BUSCA NA API + SALVAMENTO NO BANCO ---")
    print("ID Fake gerado para o Banco de dados:", cenario["novo_registro(_id)"])
    print("Dados do Livro retornados:", cenario["dados"])
    print("Resultado do Service:", resultado_service)
    
    assert resultado_service is not None
    assert str(cenario["dados"]["id"]) == "3" 
    assert cenario["novo_registro(_id)"] is not None 


def test_findByTitleDB(service, service_findByTitle):
    termo_busca = "Crime"
    
    livros_esperados = service_findByTitle(termo_busca)
    resultado = service.findByTitle(termo_busca)
    
    print("\n--- CENÁRIO: ENCONTRADO NO BANCO ---")
    print(f"Livros retornados pelo mock: {[l.titulo for l in livros_esperados]}")
    print(f"Resultado do Service: {[l.titulo for l in resultado]}")
    
    assert len(resultado) > 0
    assert resultado[0].titulo == "Crime E Castigo"
    assert resultado[0].sobre is not None  


def test_findByTitleApi(service, service_findByTitle):
    termo_busca = "1984"
    
    livros_esperados = service_findByTitle(termo_busca)
    resultado = service.findByTitle(termo_busca)
    
    print("\n--- CENÁRIO: ENCONTRADO APENAS NA API ---")
    print(f"Livros convertidos da API pela fixture: {[l.titulo for l in livros_esperados]}")
    print(f"Resultado do Service via Fallback: {[l.titulo for l in resultado]}")
    
    assert len(resultado) > 0
    assert resultado[0].titulo == "1984"
    assert resultado[0].sobre is None


def test_findAll(service, service_findAll):
    livros_esperados = service_findAll()
    resultado_livros = service.findAll()

    print("\n--- LIVROS RETORNADOS PELO SERVICE ---")
    for livro in resultado_livros:
        print(f"Título Formatado no Service: {livro.titulo} | Autor: {livro.autor}")

    assert resultado_livros is not None
    assert isinstance(resultado_livros, list)
    assert len(resultado_livros) == len(livros_esperados)

    assert resultado_livros[0].titulo == "Crime E Castigo"
    assert resultado_livros[1].titulo == "Orgulho E Preconceito"
    assert resultado_livros[2].titulo == "A Revolução Silenciosa"

