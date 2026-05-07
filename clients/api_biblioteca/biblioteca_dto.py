from pydantic import BaseModel

class Bibliotecas_dto_response(BaseModel):
    id: int
    titulo: str
    autor: str
    editora: str
