from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from prometheus_client import Histogram
from sqlalchemy.orm import Session

import crud, schemas
from api import deps

router = APIRouter()

REQUEST_TIME_BACKET = Histogram('request_latency_seconds', 'Time spent processing request', ['endpoint'])


@router.post("/", response_model=schemas.User)
@REQUEST_TIME_BACKET.labels(endpoint='/user').time()
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = crud.user.is_user_exists(db, username=user_in.username, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with same username or email already exists.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user
