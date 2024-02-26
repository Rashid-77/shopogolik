from typing import Any, List
from uuid import UUID

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
    "notify_request_latency_seconds", "Time spent processing request", ["endpoint"]
)


@router.get("/{notify_id}", response_model=List[schemas.Notify])
@REQUEST_TIME_BACKET.labels(endpoint="notify").time()
def get_notify(
    notify_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get notify by notify_id.
    """
    logger.info("get_notify()")
    notify = crud.notify.get(db, notify_id)
    if not notify:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    if notify.client_id == current_user.id or current_user.is_superuser:
        return notify

    raise HTTPException(
        status_code=400, detail="The user doesn't have enough privilege"
    )


@router.get("/order/{order_uuid}", response_model=schemas.Notify)
@REQUEST_TIME_BACKET.labels(endpoint="notify").time()
def get_notify_by_order(
    order_uuid: UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get last notify by order_uuid.
    """
    logger.info("get_notifies()")
    notify = crud.notify.get_by_order_id(db, order_uuid)
    if notify is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    if notify.client_id == current_user.id or current_user.is_superuser:
        return notify

    raise HTTPException(
        status_code=400, detail="The user doesn't have enough privilege"
    )
