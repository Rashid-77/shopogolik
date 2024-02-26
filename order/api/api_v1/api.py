from api.api_v1.endpoints import orders, ping
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(ping.router, prefix="/ping", tags=["ping"])
api_router.include_router(orders.router, prefix="/order", tags=["order"])
