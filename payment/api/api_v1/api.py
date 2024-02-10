from fastapi import APIRouter

from api.api_v1.endpoints import ping, balance

api_router = APIRouter()
api_router.include_router(ping.router, prefix="/payment/ping", tags=["ping"])
api_router.include_router(balance.router, prefix="/balance", tags=["balance"])
