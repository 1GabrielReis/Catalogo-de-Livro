from fastapi import APIRouter, HTTPException

from .route_Exception import Route_Exception
from ..controller.livro_controller import Livro_controller
from ..schemas.livro_schema import Livro_schema 

routes = APIRouter()
controller = Livro_controller()

@routes.post("/")
async def insert(schema:Livro_schema):
    try:
        return await controller.insert(schema)
    except Route_Exception as erro:
        raise HTTPException(status_code=500, detail=f"Erro insert routes \ninfo {erro}")

@routes.put("/{id}")
async def update(id:int, schema:Livro_schema):
    try:
        schema.id=id
        return await controller.update(schema)
    except Route_Exception as erro:
        raise HTTPException(status_code=500, detail=f"Erro update routes \ninfo {erro}")

@routes.delete("/{id}")
async def deleteById(id: str):
    try:
        if not id or not id.strip():
            raise HTTPException(status_code=400, detail="Dados inválidos")
        return await controller.deleteById(id)
    except Route_Exception as erro:
        raise HTTPException(status_code=500, detail=f"Erro delete routes \ninfo {erro}")

@routes.get("/id/{id}")
async def findById(id: str):
    try:
        livro = await controller.findById(id)
        if not livro:
            raise HTTPException(status_code=404, detail="Livro não encontrado")
        return livro
    except Route_Exception as erro:
        raise HTTPException(status_code=500, detail=f"Erro findById routes \ninfo {erro}")

@routes.get("/title/{title}")
async def findByTitle(title:str):
    try:
        livros = await controller.findByTitle(title)
        if not livros:
            raise HTTPException(status_code=404, detail="Livro não encontrado")
        return livros
    except Route_Exception as erro:
            raise HTTPException(status_code=500, detail=f"Erro findByTitle routes \ninfo {erro}")

@routes.get("/")
async def findAll():
    try:
        livros = await controller.findAll()
        if not livros:
            raise HTTPException(status_code=404, detail="Livro não encontrado")
        return livros
    except Route_Exception as erro:
            raise HTTPException(status_code=500, detail=f"Erro findAll routes \ninfo {erro}")