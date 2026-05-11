from pydantic import BaseModel, Field

class Livro_dto_response(BaseModel):
    id = int 
    titulo: str = Field(alias="tituto")
    autor: str
    editora: str
