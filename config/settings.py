from pathlib import Path
from dotenv import load_dotenv

from .config_exception import Config_Exception

# Encontra o caminho do arquivo .env na raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

class Settings:
    def  __init__(self,
                    data_base_url:str,
                    data_base:str,
                    ia_key:str,
                    model_id:str,
                    biblioteca_url:str,
                    blioteca_user:str
                ):
        self.data_base_url =  data_base_url
        self.data_base = data_base
        self.ia_key= ia_key
        self.model_id= model_id
        self.biblioteca_url= biblioteca_url 
        self.blioteca_user= blioteca_user
        self._validar()


    def _validar(self):
        obrigatorios = {
            "DATABASE_URL": self.data_base_url,
            "DATABASE": self.data_base,
            "IA_KEY": self.ia_key,
            "MODEL_ID": self.model_id,
            "BIBLIOTECA_URL": self.biblioteca_url,
            "BIBLIOTECA_USER": self.blioteca_user,
        }

        faltando = [nome for nome, valor in obrigatorios.items() if not valor or not str(valor).strip()]
    
        if faltando:
            raise Config_Exception(
                f"Variáveis de ambiente ausentes ou vazias: {', '.join(faltando)}. "
                f"Verifique o arquivo .env."
            )
