from fastapi import APIRouter

from api.api_v1.endpoints import login, users, ping

api_router = APIRouter()
api_router.include_router(ping.router, prefix="/ping", tags=["ping"])
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/user", tags=["user"])
