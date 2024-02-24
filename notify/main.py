import logging

from api.api_v1.api import api_router
from exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
    unhandled_exception_handler,
)
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from middleware import log_request_middleware
from prometheus_client import make_asgi_app
from starlette.exceptions import HTTPException
from utils import get_settings

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname).1s %(message)s",
    datefmt="%Y.%m.%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(api_router, prefix=get_settings().API_V1_STR)

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

app.middleware("http")(log_request_middleware)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)
