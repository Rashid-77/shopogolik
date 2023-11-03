import time
from fastapi import FastAPI

from api.api_v1.api import api_router

from utils import get_settings

import logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname).1s %(message)s",
    datefmt="%Y.%m.%d %H:%M:%S",
)
    

app = FastAPI()

app.include_router(api_router, prefix=get_settings().API_V1_STR)
