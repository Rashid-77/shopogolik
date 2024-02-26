from typing import Any

import crud
import models
import schemas
from api import deps
from fastapi import APIRouter, Depends, HTTPException, status
from prometheus_client import Histogram
from sqlalchemy.orm import Session

router = APIRouter()

REQUEST_TIME_BACKET = Histogram(
    "request_latency_seconds", "Time spent processing request", ["endpoint"]
)


@router.post("/register", response_model=schemas.User)
@REQUEST_TIME_BACKET.labels(endpoint="/courier").time()
def create_courier(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    Create new courier.
    """
    user = crud.user.is_user_exists(db, username=user_in.username, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with same username or email already exists.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=schemas.User)
@REQUEST_TIME_BACKET.labels(endpoint="/courier").time()
def read_courier_by_id(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific courier by id.
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
@REQUEST_TIME_BACKET.labels(endpoint="/courier").time()
def update_courier(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a courier.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    if user.id == current_user.id or current_user.is_superuser:
        return crud.user.update(db, db_obj=user, obj_in=user_in)
    raise HTTPException(
        status_code=400, detail="The user doesn't have enough privileges"
    )


@router.delete("/{user_id}", response_model=schemas.User)
@REQUEST_TIME_BACKET.labels(endpoint="/courier").time()
def delete_courier(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
) -> Any:
    """
    Delete a courier.
    """
    user = crud.user.remove(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this user id does not exist in the system",
        )
    return user
