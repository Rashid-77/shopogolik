from fastapi import APIRouter

from api.api_v1.endpoints import ping, product, stock

api_router = APIRouter()
api_router.include_router(ping.router, prefix="/ping", tags=["ping"])
api_router.include_router(product.router, prefix="/product", tags=["product"])
api_router.include_router(stock.router, prefix="/stock/product", tags=["stock"])

