from fastapi import APIRouter, HTTPException, status

from .route_Exception import Route_Exception
from controller.livro_controller import Livro_controller
from schemas.livro_schema import Livro_schema 


def get_livro_router(controller: Livro_controller):
    routes = APIRouter()

    @routes.post("/", status_code=status.HTTP_200_OK, summary="Criar novo livro")
    def insert(schema:Livro_schema):
        try:
            return controller.insert(schema)
        except Route_Exception as erro:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro insert routes \ninfo {erro}")

    @routes.put("/{id}", status_code=status.HTTP_200_OK, summary="Alterar livro por ID")
    def update(id:str, schema:Livro_schema):
        try:
            return controller.update(livro_schema=schema, id=id)
        except Route_Exception as erro:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro update routes \ninfo {erro}")

    @routes.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary='Deletar livro por ID')
    def deleteById(id: str):
        try:
            if not id or not id.strip():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Dados inválidos")
            return controller.deleteById(id)
        except Route_Exception as erro:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro delete routes \ninfo {erro}")

    @routes.get("/id/{id}", status_code=status.HTTP_200_OK, summary="Encontrar livro por ID")
    def findById(id: str):
        try:
            livro = controller.findById(id)
            if not livro:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado")
            return livro
        except Route_Exception as erro:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro findById routes \ninfo {erro}")

    @routes.get("/title/{title}", status_code=status.HTTP_200_OK, summary="Encontrar livro por Titulo")
    def findByTitle(title:str):
        try:
            livros = controller.findByTitle(title)
            if not livros:
                raise HTTPException(status_code=404, detail="Livro não encontrado")
            return livros
        except Route_Exception as erro:
                raise HTTPException(status_code=500, detail=f"Erro findByTitle routes \ninfo {erro}")

    @routes.get("/", status_code=status.HTTP_200_OK, summary="Listar todos os livros")
    def findAll():
        try:
            livros = controller.findAll()
            if not livros:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado")
            return livros
        except Route_Exception as erro:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERRORs, detail=f"Erro findAll routes \ninfo {erro}")
    
    return routes