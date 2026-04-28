from pydantic import BaseModel

from typing import Optional

from ..entities.livro import Livro

class Livro_schema(BaseModel):
    id: Optional[str]
    titulo: str
    autor: str
    editora: str
    sobre: str