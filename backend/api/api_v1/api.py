from fastapi import APIRouter

from backend.api.api_v1.endpoints import login, users

api_router = APIRouter()
api_router.include_router(users.router, prefix="/user", tags=["user"])
