from unittest.mock import MagicMock, patch

import pytest

from clients.api_ia.ia_exception import IA_exception


def test_retorno(ia_client, livro_dto):
    mock_resposta_gemini = MagicMock()
    mock_resposta_gemini.text = "Resumo fictício do livro Crime e Castigo gerado pelo Mock."

    url ="google.genai.models.Models.generate_content"

    with patch(url, return_value=mock_resposta_gemini):
        resposta = ia_client.about_book(livro_dto)
    
    print(str(resposta.sobre))
    assert resposta is not None
    assert "Resumo fictício" in resposta.sobre


def test_retorno_erro_api(ia_client, livro_dto):
    class FakeAPIError(Exception):
        def __init__(self, message="erro", code=429):
            super().__init__(message)
            self.code = code
            self.status_code = code

    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = FakeAPIError("quota excedida", 429)

    with patch("clients.api_ia.ia_api_client.APIError", FakeAPIError):
        with patch.object(ia_client.settings, "ia_client", return_value=mock_client):
            with pytest.raises(IA_exception):
                ia_client.about_book(livro_dto)