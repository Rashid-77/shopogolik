from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from prometheus_client import Histogram
from sqlalchemy.orm import Session

import crud, schemas, models
from api import deps
from logger import logger


router = APIRouter()

REQUEST_TIME_BACKET = Histogram('request_latency_seconds', 'Time spent processing request', ['endpoint'])


@router.post("/create", response_model=schemas.Order)
@REQUEST_TIME_BACKET.labels(endpoint='/order').time()
def create_order(
    order_in: schemas.OrderCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new order.
    """
    order = crud.order.is_order_exists(db, id=order_in.id)
    logger.info(f"{order=}")
    if order:
        raise HTTPException(
            status_code=400,
            detail="A order with same id already exists.",
        )
    return crud.order.create(db, obj_in=order_in, user_id=current_user.id)


@router.get("/{order_id}", response_model=schemas.Order)
@REQUEST_TIME_BACKET.labels(endpoint='/order').time()
def read_order_by_id(
    order_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get order by id.
    """
    logger.info("read_order_by_id()")
    order = crud.order.get(db, id=order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    if order.userId == current_user.id or current_user.is_superuser:
        return order
    raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")


@router.put("/{order_id}", response_model=schemas.Order)
@REQUEST_TIME_BACKET.labels(endpoint='/order').time()
def update_order(
    *,
    db: Session = Depends(deps.get_db),
    order_id: int,
    order_in: schemas.OrderUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update order.
    """
    logger.info("update_order()")
    order = crud.order.get(db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.userId == current_user.id or current_user.is_superuser:
        order = crud.order.update(db, db_obj=order, obj_in=order_in)
        return order
    raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")


@router.delete("/{order_id}", response_model=schemas.Order)
@REQUEST_TIME_BACKET.labels(endpoint='/order').time()
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    order_id: int,
) -> Any:
    """
    Delete order.
    """
    logger.info("delete_user()")
    order = crud.order.remove(db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
