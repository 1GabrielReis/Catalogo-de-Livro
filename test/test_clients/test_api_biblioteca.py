from unittest.mock import MagicMock, patch

import httpx
import pytest

from clients.api_biblioteca.biblioteca_exception import Biblioteca_exception


def test_findById(biblioteca_client):
    mock_resposta_http = MagicMock() 
    mock_resposta_http.status_code = 200
    mock_resposta_http.json.return_value = mock_resposta_http.json.return_value = {
        "status": "sucesso",
        "dados": {
            "id": 8,
            "titulo": "O Alquimista",
            "autor": "Paulo Coelho",
            "editora": "Rocco"
        }
    }

    comando = "httpx.Client.get"
    with patch(comando,return_value = mock_resposta_http):
        resposta = biblioteca_client.findById(8)
        print("\n" + str(resposta))
        assert resposta is not None
        assert resposta.titulo == "O Alquimista"
        assert resposta.id == "8"


def test_findByTitle(biblioteca_client):
    mock_resposta_http = MagicMock() 
    mock_resposta_http.status_code = 200
    mock_resposta_http.json.return_value = mock_resposta_http.json.return_value = {
        "status": "sucesso",
        "dados": [{
            "id": 8,
            "titulo": "O Alquimista",
            "autor": "Paulo Coelho",
            "editora": "Rocco"
        }]
    }

    comando = "httpx.Client.get"
    with patch(comando,return_value = mock_resposta_http):
        resposta = biblioteca_client.findByTitle('O Alquimista')
        print("\n" + str(resposta))
        assert resposta is not None
        assert resposta[0].titulo == "O Alquimista"


def test_findById_erro_requisicao(biblioteca_client):
    with patch("clients.api_biblioteca.biblioteca_api_client.httpx.Client") as client_cls:
        mock_client = client_cls.return_value.__enter__.return_value
        mock_client.get.side_effect = httpx.ConnectError("falha de rede")

        with pytest.raises(Biblioteca_exception):
            biblioteca_client.findById(8)
