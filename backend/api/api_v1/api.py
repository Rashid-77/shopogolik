from fastapi import APIRouter

from api.api_v1.endpoints import login, users, metrics

api_router = APIRouter()
api_router.include_router(users.router, prefix="/user", tags=["user"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
