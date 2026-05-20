from fastapi import APIRouter
from ..view.response_interface import Response_interface
from ..schemas.livro_schema import Livro_schema
from ..service.livro_service import Livro_service

router = APIRouter()

class Livro_handler():
    def __init__(self,router:function, service:Livro_service, view:Response_interface):
        self.router = router
        self.service = service
        self.view = view
    
    
