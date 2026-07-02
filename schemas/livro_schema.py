from pydantic import BaseModel

from typing import Optional

class Livro_schema(BaseModel):
    id: Optional[str]
    titulo: str
    autor: str
    editora: str
    sobre: Optional[str]