from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from prometheus_client import Histogram
from sqlalchemy.orm import Session

import crud, schemas, models
from api import deps
from logger import logger


router = APIRouter()

REQUEST_TIME_BACKET = Histogram('courier_request_latency_seconds', 'Time spent processing request', ['endpoint'])


@router.get("/{notify_id}", response_model=List[schemas.Notify])
@REQUEST_TIME_BACKET.labels(endpoint='courier').time()
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

    raise HTTPException(status_code=400, detail="The user doesn't have enough privilege")


@router.get("/order/{order_uuid}", response_model=schemas.Notify)
@REQUEST_TIME_BACKET.labels(endpoint='courier').time()
def get_notify(
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
    
    if notify.client_id==current_user.id or current_user.is_superuser:
        return notify

    raise HTTPException(status_code=400, detail="The user doesn't have enough privilege")


# @router.put("/{user_id}", response_model=schemas.Courier)
# @REQUEST_TIME_BACKET.labels(endpoint='/courier').time()
# def update_user(
#     *,
#     db: Session = Depends(deps.get_db),
#     user_id: int,
#     user_in: schemas.CourierUpdate,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Update a user.
#     """
#     logger.info("add_courier()")

#     if current_user.is_superuser:
#         u = crud.user.get(db, id=user_id)
#         if not u:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
#         if not crud.user.is_active(u):
#             raise HTTPException(status_code=422, detail="User is not active.")
    
#     cu = crud.courier.get_courier_id(db, user_id=user_id)
#     if cu is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, 
#             detail="Courier not in list"
#         )
#     cu = crud.courier.update(db, db_obj=cu, obj_in=user_in)
#     return cu


# @router.delete("/{user_id}", response_model=schemas.Courier)
# @REQUEST_TIME_BACKET.labels(endpoint='/courier').time()
# def delete_courier(
#     *,
#     db: Session = Depends(deps.get_db),
#     user_id: int,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Delete courier.
#     """
#     logger.info("delete_courier()")
#     courier = crud.courier.remove(db, user_id=user_id)
#     if not courier:
#         raise HTTPException(status_code=404, detail="Courier not found")
#     if current_user.is_superuser:
#         return courier
#     raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")
