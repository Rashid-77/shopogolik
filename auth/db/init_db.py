import os

import schemas  # noqa: F401
from sqlalchemy.orm import Session

import crud
from . import base  # noqa: F401
from utils.config import get_settings
# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # from db.base_class import Base
    # from db.session import engine

    # Base.metadata.create_all(bind=engine)

    email = get_settings().first_superuser
    passw = get_settings().first_superuser_password
    user = crud.user.get_by_email(db, email=email)
    if not user:
        user_in = schemas.UserCreate(
            username=email,
            email=email,
            password=passw,
            is_superuser=True,
        )
        user = crud.user.create(db, obj_in=user_in)  # noqa: F841
    pass
