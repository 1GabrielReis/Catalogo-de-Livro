import os
from pathlib import Path
from dotenv import load_dotenv

# Encontra o caminho do arquivo .env na raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

class Settings:
    #---Data base ---
    DATABASE_URL: str = os.getenv("DATABASE_URL") 
    DATABASE: str = os.getenv("DATABASE")

    #--- Clients ---
    # ia
    IA_KEY: str = os.getenv("IA_KEY") 
    MODEL_ID: str = os.getenv("MODEL_ID") 
    # biblioteca
    BIBLIOTECA_URL: str = os.getenv("BIBLIOTECA_URL") 
    USERNAME: str = os.getenv("USERNAME")
