from api.api_v1.endpoints import notify, ping
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(ping.router, prefix="/notify/ping", tags=["ping"])
api_router.include_router(notify.router, prefix="/notify", tags=["notify"])
