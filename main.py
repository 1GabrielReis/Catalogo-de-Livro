import sys
import os
from contextlib import asynccontextmanager 
from fastapi import  FastAPI

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from api import route
from config import settings, container as cont
from database.migrations import generate_book_collection as db_collection
from database.migrations import generate_book_indexes as db_indexes
from database.seeds import initial_data as db_initial

from controller.livro_controller import Livro_controller
from view.view_entities.livro_view import Livro_view

app = FastAPI(lifespan=lambda app: lifespan(app))

# setting 
settings_env = settings.Settings(data_base_url= os.getenv('DATABASE_URL'),
                        data_base= os.getenv('DATABASE'),
                        ia_key= os.getenv('IA_KEY'),
                        model_id= os.getenv('MODEL_ID'),
                        biblioteca_url= os.getenv('BIBLIOTECA_URL'),
                        blioteca_user= os.getenv('BIBLIOTECA_USER'))

container= cont.Container(settings_env)

def run_database_migrations():
    create_collection_indexes =  False
    create_initial_data = False

    if create_collection_indexes:
        db_collection.up(container.get("db"))
        db_indexes.up(container.get("db"))

    if create_initial_data:
        db_initial.up(container.get("db"))

def configure_application_routes(app: FastAPI):
    controller = Livro_controller(service=container.get('Livro_service'), view=Livro_view())
    livro_router = route.get_livro_router(controller)
    app.include_router(livro_router,prefix="/livro",tags=["Livro"])

@asynccontextmanager
async def lifespan(app: FastAPI):
    data_base = container.get('db')
    
    run_database_migrations()
    configure_application_routes(app)
    
    yield 
    
    data_base.disconnect()