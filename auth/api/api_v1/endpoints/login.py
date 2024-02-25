from datetime import timedelta
from typing import Annotated, Any

import crud
import models
import schemas
from api import deps
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from logger import logger
from pydantic import ValidationError
from sqlalchemy.orm import Session
from utils import security
from utils.security import decode_access_token  # noqa

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    logger.info("")
    logger.info("-->login_access_token()")

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


@router.get("/signin")
def signin() -> Any:
    """
    Redirection to the login page
    """
    return {"message": "Please go to login and provide Login/Password"}


oath_jwt_token = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/auth")  # , response_model=schemas.XAuthHeaders)
def authenticate(
    # authorization: Annotated[str | None, Header()] = None,
    token: Annotated[str, Depends(oath_jwt_token)],
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Authenticate user
    """

    logger.info("--> authenticate()")
    # scheme, _, token = authorization.partition(" ")

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        # token_data = TokenData(user_id=user_id)
    except (JWTError, ValidationError):
        raise credentials_exception

    current_user = crud.user.get(db, id=user_id)
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    response = Response()
    response.headers["X-UserId"] = str(current_user.id)
    response.headers["X-User"] = str(current_user.username)
    response.headers["X-First-Name"] = str(current_user.first_name)
    response.headers["X-Last-Name"] = str(current_user.last_name)
    response.headers["X-Email"] = str(current_user.email)
    response.headers["X-Phone"] = str(current_user.phone)
    response.headers["X-Superuser"] = str(current_user.is_superuser)

    return response
