from typing import Any

import crud
import models
import schemas
from api import deps
from fastapi import APIRouter, Depends, HTTPException, status
from logger import logger
from prometheus_client import Histogram
from sqlalchemy.orm import Session

router = APIRouter()

REQUEST_TIME_BACKET = Histogram(
    "stock_request_latency_seconds", "Time spent processing request", ["endpoint"]
)


@router.post("/add", response_model=schemas.Stock)
@REQUEST_TIME_BACKET.labels(endpoint="/stock").time()
def add_product_to_stock(
    product_in: schemas.StockCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Add product to stock.
    """
    logger.info("add_product_to_stock()")
    stock = crud.stock.is_prod_id_exists(db, prod_id=product_in.prod_id)
    logger.info(f"{stock=}")
    if stock:
        raise HTTPException(
            status_code=400,
            detail="A product with same prod_id already exists.",
        )
    if current_user.is_superuser:
        return crud.stock.create(db, obj_in=product_in)
    raise HTTPException(
        status_code=400, detail="The user doesn't have enough privilege"
    )


@router.get("/{prod_id}", response_model=schemas.Stock)
@REQUEST_TIME_BACKET.labels(endpoint="/stock").time()
def read_product_by_id_in_stock(
    prod_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get product details in stock.
    """
    logger.info("read_product_by_id_in_stock()")
    stock = crud.stock.get_by_prod_id(db, prod_id=prod_id)
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return stock


@router.put("/{prod_id}", response_model=schemas.Stock)
@REQUEST_TIME_BACKET.labels(endpoint="/stock").time()
def update_product_in_stock(
    *,
    db: Session = Depends(deps.get_db),
    prod_id: int,
    stock_in: schemas.StockUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update product details in stock.
    """
    logger.info("update_product_in_stock()")
    stock = crud.stock.is_prod_id_exists(db, prod_id=prod_id)
    if current_user.is_superuser:
        stock_in.prod_id = prod_id
        if stock:
            return crud.stock.update(db, db_obj=stock, obj_in=stock_in)
        return crud.stock.create(db, obj_in=stock_in)
    raise HTTPException(
        status_code=400, detail="The user doesn't have enough privileges"
    )


@router.delete("/{stock_id}", response_model=schemas.Stock)
@REQUEST_TIME_BACKET.labels(endpoint="/stock").time()
def delete_product_from_stock(
    *,
    db: Session = Depends(deps.get_db),
    stock_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete product from stock.
    """
    logger.info("delete_product_from_stock()")
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    stock = crud.stock.remove(db, id=stock_id)
    if not stock:
        raise HTTPException(
            status_code=404, detail="Product details not found in stock"
        )
    return stock
