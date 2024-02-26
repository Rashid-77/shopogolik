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
    "request_latency_seconds", "Time spent processing request", ["endpoint"]
)


@router.get("/me", response_model=schemas.User)
@REQUEST_TIME_BACKET.labels(endpoint="/user").time()
def read_user_me(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a current user info.
    """
    logger.info("read_user_me()")
    current_user.id = int(current_user.id)
    return current_user


@router.get("/{user_id}", response_model=schemas.User)
@REQUEST_TIME_BACKET.labels(endpoint="/user").time()
def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    if user.id == current_user.id or current_user.is_superuser:
        return user
    raise HTTPException(
        status_code=400, detail="The user doesn't have enough privileges"
    )


@router.put("/{user_id}", response_model=schemas.User)
@REQUEST_TIME_BACKET.labels(endpoint="/user").time()
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
) -> Any:
    """
    Update a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this user id does not exist in the system",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/{user_id}", response_model=schemas.User)
@REQUEST_TIME_BACKET.labels(endpoint="/user").time()
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
) -> Any:
    """
    Delete a user.
    """
    user = crud.user.remove(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this user id does not exist in the system",
        )
    return user
