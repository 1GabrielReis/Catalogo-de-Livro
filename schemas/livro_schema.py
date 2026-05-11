from pydantic import BaseModel
from datetime import date

from typing import Optional

class Livro_schema(BaseModel):
    id: Optional[str]
    titulo: str
    autor: str
    editora: str
    sobre: Optional[str]
    data_criacao: Optional[date]