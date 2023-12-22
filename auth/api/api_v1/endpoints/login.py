from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import crud, schemas, models
from api import deps
from utils import security
from logger import logger

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    logger.info("")
    logger.info('-->login_access_token()')
    
    user = crud.user.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/logout", response_model=schemas.Token)
def logout(current_user: models.User = Depends(deps.get_current_active_user)) -> Any:
    """
    Logut from system
    """
    return {
        "access_token": "",
        "token_type": "bearer",
    }


@router.post("/auth")# , response_model=schemas.XAuthHeaders)
def authenticate(current_user: models.User = Depends(deps.get_current_active_user)) -> Any:
    """
    Authenticate user
    """
    logger.info("--> authenticate()")
    response = Response()
    response.headers["X-UserId"] = str(current_user.id)
    response.headers["X-User"] = str(current_user.username)
    response.headers["X-First-Name"] = str(current_user.first_name)
    response.headers["X-Lirst-Name"] = str(current_user.last_name)
    response.headers["X-Email"] = str(current_user.email)
    response.headers["X-Phone"] = str(current_user.phone)

    return response
