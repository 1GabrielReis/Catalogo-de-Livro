from google.api_core import exceptions

from ..api_biblioteca.livro_dto_response import Livro_dto_response

from ..clients_interface import IIa_interface
from .ia_settings import IA_settings
from .ia_dto_response import IA_dto_response
from .ia_exception import IA_exception
from models.entities.livro import Livro

class IA_api_client(IIa_interface):
    def __init__(self, settings: IA_settings):
        self.settings = settings
    
    
    def about_book(self,livro : Livro_dto_response | Livro) -> IA_dto_response:
        try:
            client = self.settings.ia_client()

            prompt= f''' Atue como um analista literário. Forneça um resumo objetivo e os 
                        principais tópicos abordados no livro:
                        Título: {livro.titulo}
                        Autor: {livro.autor}
                        Editora: {livro.editora}- Opcional
                        Estrutura da resposta:
                        Resumo Geral: (3 a 5 parágrafos sobre a ideia central).
                        Público-alvo: (Para quem este livro é recomendado).
                        Estilo de Escrita: (Diga se a leitura é técnica, fluida ou densa).
                        Use uma linguagem clara e direta.
                        a resposta poder ter no maximo 1000 caracteres
                    '''
            response = client.models.generate_content(model=self.settings.MODEL_ID,contents=prompt)
            
            sobre = response.text
            livro_dict =  livro.__dict__ if not hasattr(livro, 'model_dump') else livro.model_dump()

            return IA_dto_response(**livro_dict,sobre=sobre)

        except exceptions.ResourceExhausted as erro:
            raise IA_exception(f"Limite de requisições atingido. Calma lá!\ninfo:{erro}")
        except exceptions.InvalidArgument as erro:
            raise IA_exception(f"Erro nos parâmetros \ninfo:{erro}")
        except exceptions.GoogleAPIError as erro:
            raise IA_exception(f"Erro interno na API de IA.\ninfo:{erro}")
        except Exception as erro:
            raise IA_exception(f'Erro inesperado. Camda de API IA \ninfo: {erro}')
