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
    "product_request_latency_seconds", "Time spent processing request", ["endpoint"]
)


@router.post("/add", response_model=schemas.Product)
@REQUEST_TIME_BACKET.labels(endpoint="/product").time()
def add_product(
    product_in: schemas.ProductCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new product.
    """
    logger.info("add_product()")
    pass
    product = crud.product.is_product_exists(db, name=product_in.name)
    logger.info(f"{product=}")
    if product:
        raise HTTPException(
            status_code=400,
            detail="A product with same name already exists.",
        )
    logger.info(f"{current_user.username=}")
    logger.info(f"{current_user.is_superuser=}")
    if current_user.is_superuser:
        return crud.product.create(db, obj_in=product_in)
    raise HTTPException(
        status_code=400, detail="The user doesn't have enough privilege"
    )


@router.get("/{product_id}", response_model=schemas.Product)
@REQUEST_TIME_BACKET.labels(endpoint="/product").time()
def read_product_by_id(
    product_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get product by id.
    """
    logger.info("read_product_by_id()")
    product = crud.product.get(db, id=product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return product


@router.put("/{product_id}", response_model=schemas.Product)
@REQUEST_TIME_BACKET.labels(endpoint="/product").time()
def update_product(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int,
    product_in: schemas.ProductUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update product.
    """
    logger.info("update_product()")
    product = crud.product.get(db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if current_user.is_superuser:
        return crud.product.update(db, db_obj=product, obj_in=product_in)
    raise HTTPException(
        status_code=400, detail="The user doesn't have enough privileges"
    )


@router.delete("/{product_id}", response_model=schemas.Product)
@REQUEST_TIME_BACKET.labels(endpoint="/product").time()
def delete_product(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete product.
    """
    logger.info("delete_product()")
    product = crud.product.remove(db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if current_user.is_superuser:
        return product
    raise HTTPException(
        status_code=400, detail="The user doesn't have enough privileges"
    )
