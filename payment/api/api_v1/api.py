from api.api_v1.endpoints import balance, ping
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(ping.router, prefix="/payment/ping", tags=["ping"])
api_router.include_router(balance.router, prefix="/balance", tags=["balance"])
