import os
from pathlib import Path
from dotenv import load_dotenv

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
        self.data_base_url =  os.getenv(f"{data_base_url}")
        self.data_base = os.getenv(f"{data_base}")
        self.ia_key= os.getenv(f"{ia_key}")
        self.model_id= os.getenv(f"{model_id}")
        self.biblioteca_url= os.getenv(f"{biblioteca_url}") 
        self.blioteca_user= os.getenv(f"{blioteca_user}")

