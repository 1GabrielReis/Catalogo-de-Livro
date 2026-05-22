from fastapi import APIRouter
from ..controller.livro_controller import Livro_controller
from ..schemas.livro_schema import Livro_schema 

routes = APIRouter()
controller = Livro_controller()

@routes.post("/")
async def insert(schema:Livro_schema):
    return await controller.insert(schema)

@routes.put("/{id}")
async def update(id:int, schema:Livro_schema):
    schema.id=id
    return await controller.update(schema)

@routes.delete("/{id}")
async def deleteById(id: str):
    return await controller.deleteById(id)

@routes.get("/id/{id}")
async def findById(id: str):
    return await controller.findById(id)

@routes.get("/title/{title}")
async def findByTitle(title:str):
    return await controller.findByTitle(title)

@routes.get("/")
async def findAll():
    return await controller.findAll()