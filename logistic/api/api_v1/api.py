from api.api_v1.endpoints import logistic, ping, users
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(ping.router, prefix="/logistic/ping", tags=["ping"])
api_router.include_router(logistic.router, prefix="/logistic", tags=["logistic"])
api_router.include_router(users.router, prefix="/logistic/courier", tags=["courier"])
