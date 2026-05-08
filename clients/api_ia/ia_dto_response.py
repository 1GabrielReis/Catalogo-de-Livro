from pydantic import BaseModel
from typing import Optional

class IA_dto_response(BaseModel):
    titulo: str
    autor: str
    editora: str
    sobre: Optional[str]
