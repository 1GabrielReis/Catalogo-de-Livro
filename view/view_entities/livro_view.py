from ..response_base import Response_base
from ...models.entities.livro import Livro

class Livro_view(Response_base):

    def format(self, livro: Livro) -> dict:
        livro_dict = livro.__dict__.copy()
        livro_dict['data_criacao'] = str(livro_dict['data_criacao'])
        
        return {
            "status": "sucesso",
            "dados": livro_dict
        }

    def format_list(self, livros) -> dict:
        return {
            "status": "sucesso",
            "quantidade": len(livros),
            "dados": [self.format(livro)["dados"] for livro in livros] if livros else []
        }
    
    def info(self, info: dict) -> dict:
        return {
            "status": "sucesso",
            "dados": info
        }