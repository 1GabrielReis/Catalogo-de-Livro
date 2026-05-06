from pydantic import BaseModel

class Bibliotecas_dto_response(BaseModel):
    id: int
    titutlo: str
    autor: str
    editora: str
