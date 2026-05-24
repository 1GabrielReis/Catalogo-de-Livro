import os
from pathlib import Path
from dotenv import load_dotenv

# Encontra o caminho do arquivo .env na raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")