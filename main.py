import sys
import os
from contextlib import asynccontextmanager 
from fastapi import  FastAPI

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from api import route
from config import settings, container as cont
from database.connections.db_mongo import DB_mongo as DB
from database.migrations import generate_book_collection as db_collection
from database.migrations import generate_book_indexes as db_indexes
from database.seeds import initial_data as db_initial

from clients.api_ia.ia_settings import IA_settings 
from clients.api_biblioteca.biblioteca_settings import Biblioteca_settings
from models.dao.implementation.livro_dao_mongo import Livro_dao_mongo

from service.livro_service import Livro_service
from controller.livro_controller import Livro_controller
from view.view_entities.livro_view import Livro_view

app = FastAPI(lifespan=lambda app: lifespan(app))

# setting 
settings_env = settings.Settings(data_base_url= os.getenv('DATABASE_URL'),
                        data_base= os.getenv('DATABASE'),
                        ia_key= os.getenv('IA_KEY'),
                        model_id= os.getenv('MODEL_ID'),
                        biblioteca_url= os.getenv('BIBLIOTECA_URL'),
                        blioteca_user= os.getenv('USERNAME'))


def run_database_migrations(data_base):
    create_collection_indexes =  True
    create_initial_data = True

    if create_collection_indexes:
        db_collection.up(data_base)
        db_indexes.up(data_base)

    if create_initial_data:
        db_initial.up(data_base)

def configure_application_routes(app: FastAPI, data_base):
    # Clients / Infra
    livro_db = Livro_dao_mongo(db=data_base)
    ia_api = IA_settings(key=settings_env.ia_key, MODEL_ID=settings_env.model_id)
    bilioteca_api = Biblioteca_settings(
        base_url=settings_env.biblioteca_url,
        username=settings_env.blioteca_user
    )

    # Container IoC
    container = cont.Container(
        livro_bd=livro_db,
        biblioteca_api=bilioteca_api,
        ia_api=ia_api
    )

    # Core Domain Layer (Service)
    service = Livro_service(
        repository=container.container['ILivro_interface'],
        library_client=container.container['IBiblioteca_interface'],
        ia_client=container.container['IA_dto_response']
    )

    # Controller / View
    controller = Livro_controller(service=service, view=Livro_view())

    # Injeta o controller na fábrica de rotas
    livro_router = route.get_livro_router(controller)

    app.include_router(
        livro_router,
        prefix="/livro",
        tags=["Livro"]
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    data_base = DB(bd=settings_env.data_base_url, client=settings_env.data_base)
    
    # Chama as execuções à parte organizadas
    run_database_migrations(data_base)
    configure_application_routes(app, data_base)
    
    yield # O app roda aqui
    
    # SHUTDOWN
    data_base.disconnect()