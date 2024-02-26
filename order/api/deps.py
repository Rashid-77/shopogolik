from typing import Annotated, Generator

import crud
import models
from db.session import SessionLocal
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from logger import logger
from sqlalchemy.orm import Session
from utils.config import get_settings
from utils.security import decode_access_token  # noqa

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{get_settings().API_V1_STR}/login")


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def get_current_user(
    db: Session = Depends(get_db),
    x_userid: Annotated[str | None, Header()] = None,
    x_user: Annotated[str | None, Header()] = None,
    x_first_name: Annotated[str | None, Header()] = "",
    x_last_name: Annotated[str | None, Header()] = "",
    x_email: Annotated[str | None, Header()] = None,
    x_phone: Annotated[str | None, Header()] = "",
) -> models.User:
    logger.info("get_current_user()")
    if (
        (x_userid is None or x_userid == "")
        or (x_user is None or x_user == "")
        or (x_email is None or x_email == "")
    ):
        logger.info(
            f" {x_userid=}, {x_user=}, {x_first_name=},"
            f" {x_last_name=}, {x_email=}, {x_phone=} "
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = models.User(
        id=int(x_userid),
        username=x_user,
        first_name=x_first_name,
        last_name=x_last_name,
        email=x_email,
        phone=x_phone,
        disabled=False,
    )
    logger.info(f" {user=}")
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_current_active_user(
    current_user: Annotated[models.User, Depends(get_current_user)]
) -> models.User:
    logger.info("get_current_active_user()")
    if not crud.user.is_active(current_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
