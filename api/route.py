from fastapi import APIRouter, HTTPException

from .route_Exception import Route_Exception
from controller.livro_controller import Livro_controller
from schemas.livro_schema import Livro_schema 


def get_livro_router(controller: Livro_controller):
    routes = APIRouter()

    @routes.post("/")
    def insert(schema:Livro_schema):
        try:
            return controller.insert(schema)
        except Route_Exception as erro:
            raise HTTPException(status_code=500, detail=f"Erro insert routes \ninfo {erro}")

    @routes.put("/{id}")
    def update(id:str, schema:Livro_schema):
        try:
            return controller.update(livro_schema=schema, id=id)
        except Route_Exception as erro:
            raise HTTPException(status_code=500, detail=f"Erro update routes \ninfo {erro}")

    @routes.delete("/{id}")
    def deleteById(id: str):
        try:
            if not id or not id.strip():
                raise HTTPException(status_code=400, detail="Dados inválidos")
            return controller.deleteById(id)
        except Route_Exception as erro:
            raise HTTPException(status_code=500, detail=f"Erro delete routes \ninfo {erro}")

    @routes.get("/id/{id}")
    def findById(id: str):
        try:
            livro = controller.findById(id)
            if not livro:
                raise HTTPException(status_code=404, detail="Livro não encontrado")
            return livro
        except Route_Exception as erro:
            raise HTTPException(status_code=500, detail=f"Erro findById routes \ninfo {erro}")

    @routes.get("/title/{title}")
    def findByTitle(title:str):
        try:
            livros = controller.findByTitle(title)
            if not livros:
                raise HTTPException(status_code=404, detail="Livro não encontrado")
            return livros
        except Route_Exception as erro:
                raise HTTPException(status_code=500, detail=f"Erro findByTitle routes \ninfo {erro}")

    @routes.get("/")
    def findAll():
        try:
            livros = controller.findAll()
            if not livros:
                raise HTTPException(status_code=404, detail="Livro não encontrado")
            return livros
        except Route_Exception as erro:
                raise HTTPException(status_code=500, detail=f"Erro findAll routes \ninfo {erro}")
    
    return routes