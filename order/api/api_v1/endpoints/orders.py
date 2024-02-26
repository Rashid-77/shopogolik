from typing import Any
from uuid import UUID

import crud
import models
import schemas
from api import deps
from events_pub.order_pub import publish_order_created
from fastapi import APIRouter, Depends, HTTPException, status
from logger import logger
from prometheus_client import Histogram
from sqlalchemy.orm import Session

router = APIRouter()

REQUEST_TIME_BACKET = Histogram(
    "request_latency_seconds", "Time spent processing request", ["endpoint"]
)


@router.post("/create", response_model=schemas.Order)
# TODO change sync prometeus client to async
# @REQUEST_TIME_BACKET.labels(endpoint='/order').time()
async def create_order(
    order_in: schemas.OrderInfoCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new order.
    """
    order = crud.order.is_order_exists(db, uuid=order_in.uuid)
    if order:
        raise HTTPException(
            status_code=400,
            detail="A order with same uuid already exists.",
        )
    order_state = schemas.OrderCreate(uuid=order_in.uuid)
    order = crud.order.create(db, obj_in=order_state, user_id=current_user.id)
    publish_order_created(order_in)
    return order


@router.get("/{order_uuid}", response_model=schemas.Order)
# TODO change sync prometeus client to async
# @REQUEST_TIME_BACKET.labels(endpoint='/order').time()
async def read_order_by_id(
    order_uuid: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get order by id.
    """
    logger.info("read_order_by_id()")
    order = crud.order.get(db, uuid=order_uuid)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    if order.userId == current_user.id or current_user.is_superuser:
        return order
    raise HTTPException(
        status_code=400, detail="The user doesn't have enough privileges"
    )


@router.put("/{order_uuid}", response_model=schemas.Order)
@REQUEST_TIME_BACKET.labels(endpoint="/order").time()
async def update_order(
    *,
    db: Session = Depends(deps.get_db),
    order_uuid: UUID,
    order_in: schemas.OrderUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update order.
    """
    logger.info("update_order()")
    order = crud.order.get(db, uuid=order_uuid)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.userId == current_user.id or current_user.is_superuser:
        order = crud.order.update(db, db_obj=order, obj_in=order_in)
        return order
    raise HTTPException(
        status_code=400, detail="The user doesn't have enough privileges"
    )


@router.delete("/{order_uuid}", response_model=schemas.Order)
@REQUEST_TIME_BACKET.labels(endpoint="/order").time()
async def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    order_uuid: UUID,
) -> Any:
    """
    Delete order.
    """
    logger.info("delete_user()")
    order = crud.order.remove(db, id=order_uuid)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
