from fastapi import APIRouter

from api.api_v1.endpoints import ping

api_router = APIRouter()
api_router.include_router(ping.router, prefix="/ping", tags=["ping"])
