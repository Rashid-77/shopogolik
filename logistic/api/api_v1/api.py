from fastapi import APIRouter

from api.api_v1.endpoints import ping, logistic

api_router = APIRouter()
api_router.include_router(ping.router, prefix="/logistic/ping", tags=["ping"])
api_router.include_router(logistic.router, prefix="/logistic", tags=["logistic"])
