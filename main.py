from fastapi import APIRouter
from api.route import route 

import sys
import os 

from .config import settings as sett, container

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
router = APIRouter()


