from api.api_v1.endpoints import ping, product, stock, stock_info
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(ping.router, prefix="/product/ping", tags=["ping"])
api_router.include_router(product.router, prefix="/product", tags=["product"])
api_router.include_router(stock.router, prefix="/stock/product", tags=["stock"])
api_router.include_router(
    stock_info.router, prefix="/stock/prod-info", tags=["prod-info"]
)
