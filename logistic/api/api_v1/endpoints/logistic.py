from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from prometheus_client import Histogram
from sqlalchemy.orm import Session

import crud, schemas, models
from api import deps
from logger import logger


router = APIRouter()

REQUEST_TIME_BACKET = Histogram('courier_request_latency_seconds', 'Time spent processing request', ['endpoint'])


@router.post("/{user_id}", response_model=schemas.Courier)
@REQUEST_TIME_BACKET.labels(endpoint='courier').time()
def add_courier(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
        Add courier to logistic service
    """
    logger.info("add_courier()")

    if current_user.is_superuser:
        u = crud.user.get(db, id=user_id)
        if not u:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
        if not crud.user.is_active(u):
            raise HTTPException(status_code=422, detail="User is not active.")
        # if u.is_courier:
        #     raise HTTPException(status_code=400, detail="The user is not a courier")
        return crud.courier.create(db, user_id=user_id)
    raise HTTPException(status_code=400, detail="You doesn`t have enough privileges")


@router.get("/free-couriers", response_model=List[schemas.CourierUnoccupied])
@REQUEST_TIME_BACKET.labels(endpoint='courier').time()
def get_free_couriers(
    db: Session = Depends(deps.get_db),
    offset:int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get free couriers.
    """
    logger.info("get_free_couriers()")
    if current_user.is_superuser:
        cu = crud.courier.get_free(db, offset, limit)
        if cu is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
        return cu
    raise HTTPException(status_code=400, detail="The user doesn't have enough privilege")


@router.get("/{user_id}", response_model=schemas.Courier)
@REQUEST_TIME_BACKET.labels(endpoint='courier').time()
def get_courier(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get courier info by user_id.
    """
    logger.info("get_courier()")
    if current_user.id == user_id or current_user.is_superuser:
        cu = crud.courier.get_courier_id(db, user_id=user_id)
        if cu is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
        return cu
    raise HTTPException(status_code=400, detail="The user doesn't have enough privilege")



@router.put("/{user_id}", response_model=schemas.Courier)
@REQUEST_TIME_BACKET.labels(endpoint='/courier').time()
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: schemas.CourierUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a user.
    """
    logger.info("add_courier()")

    if current_user.is_superuser:
        u = crud.user.get(db, id=user_id)
        if not u:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
        if not crud.user.is_active(u):
            raise HTTPException(status_code=422, detail="User is not active.")
    
    cu = crud.courier.get_courier_id(db, user_id=user_id)
    if cu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Courier not in list"
        )
    cu = crud.courier.update(db, db_obj=cu, obj_in=user_in)
    return cu


@router.delete("/{user_id}", response_model=schemas.Courier)
@REQUEST_TIME_BACKET.labels(endpoint='/courier').time()
def delete_courier(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete courier.
    """
    logger.info("delete_courier()")
    courier = crud.courier.remove(db, courier_id=user_id)
    if not courier:
        raise HTTPException(status_code=404, detail="Courier not found")
    if current_user.is_superuser:
        return courier
    raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")
