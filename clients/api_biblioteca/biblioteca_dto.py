from pydantic import BaseModel, Field

class Bibliotecas_dto_response(BaseModel):
    id: int
    titulo: str = Field(alias="titutlo")
    autor: str
    editora: str
