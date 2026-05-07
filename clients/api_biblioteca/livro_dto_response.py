from pydantic import BaseModel, Field

class Livro_dto_response(BaseModel):
    titulo: str = Field(alias="titutlo")
    autor: str
    editora: str
