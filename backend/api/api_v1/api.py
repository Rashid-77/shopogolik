from fastapi import APIRouter

from api.api_v1.endpoints import users, ping

api_router = APIRouter()
api_router.include_router(ping.router, prefix="/ping", tags=["ping"])
api_router.include_router(users.router, prefix="/user", tags=["user"])
