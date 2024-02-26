from typing import Any

import crud
import schemas
from api import deps
from fastapi import APIRouter, Depends, HTTPException, status
from logger import logger
from prometheus_client import Histogram
from sqlalchemy.orm import Session

router = APIRouter()

REQUEST_TIME_BACKET = Histogram(
    "stock_info_request_latency_seconds", "Time spent processing request", ["endpoint"]
)


@router.get("/{prod_id}", response_model=schemas.Stock)
@REQUEST_TIME_BACKET.labels(endpoint="/stock").time()
def read_prod_info_in_stock(
    prod_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get product amount in stock. Using for unauthorized users.
    """
    logger.info("read_prod_info_in_stock()")
    stock = crud.stock.get_by_prod_id(db, prod_id=prod_id)
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return stock
