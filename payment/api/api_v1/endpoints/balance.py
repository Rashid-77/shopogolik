from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from prometheus_client import Histogram
from sqlalchemy.orm import Session

import crud, schemas, models
from api import deps
from logger import logger


router = APIRouter()

REQUEST_TIME_BACKET = Histogram('balance_request_latency_seconds', 'Time spent processing request', ['endpoint'])


@router.post("/deposit/{user_id}", response_model=schemas.Balance)
@REQUEST_TIME_BACKET.labels(endpoint='/balance').time()
def create_deposit(
    bal_in: schemas.BalanceCreate,
    # user_id: int,
    # depos_uuid: str,
    # amount: float,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create money deposit to in-shop account.
    depos_uuid should be unique for every deposit
    only positive amount is allowed
    """
    logger.info("create_deposit()")
    
    # acc = crud.money_account.is_exists(db, user_id=user_id)
    # logger.info(f"{acc=}")
    # if acc:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="A money account for this user already exists.",
    #     )
    logger.info(f" user_id={current_user.id}, admin={current_user.is_superuser}, "
                f"amount={bal_in.amount}")

    if current_user.id == bal_in.user_id or current_user.is_superuser:
        if bal_in.amount < 0:
            raise HTTPException(status_code=422, detail="Unprocessable Entity.")
        acc = crud.money_account.create(db, bal_in.user_id, bal_in.depos_uuid, bal_in.amount)
        if acc is None:
            raise HTTPException(status_code=422, detail="Unprocessable Entity.")
        return acc
    raise HTTPException(status_code=400, detail="The user doesn't have enough privilege")


@router.get("/{user_id}", response_model=schemas.BalanceNow)
@REQUEST_TIME_BACKET.labels(endpoint='/balance').time()
def read_balance(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get user balance by user_id.
    """
    logger.info("read_balance()")
    if current_user.id == user_id or current_user.is_superuser:
        acc = crud.money_account.get_balance(db, user_id=user_id)
        if acc is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
        logger.info(f"{acc=}, {type(acc)=}")
        return acc
    raise HTTPException(status_code=400, detail="The user doesn't have enough privilege")


# @router.put("/{user_id}", response_model=schemas.Product)
# @REQUEST_TIME_BACKET.labels(endpoint='/balance').time()
# def update_balance(
#     user_id: int,
#     amount: float,
#     db: Session = Depends(deps.get_db),
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Update balance.
#     """
#     logger.info("update_balance()")
#     acc = crud.money_account.get_by_user_id(db, user_id=user_id)
#     if not acc:
#         raise HTTPException(status_code=404, detail="User money account not found")
#     if current_user.id == user_id or current_user.is_superuser:
#         acc = crud.money_account.update(db, user_id=user_id, amount=amount)
#         if acc is None:
#             raise HTTPException(status_code=422, detail="Unprocessable Entity.")
#         return acc
#     raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")


# @router.delete("/{product_id}", response_model=schemas.Product)
# @REQUEST_TIME_BACKET.labels(endpoint='/product').time()
# def delete_product(
#     *,
#     db: Session = Depends(deps.get_db),
#     product_id: int,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Delete product.
#     """
#     logger.info("delete_product()")
#     product = crud.product.remove(db, id=product_id)
#     if not product:
#         raise HTTPException(status_code=404, detail="Product not found")
#     if current_user.is_superuser:
#         return product
#     raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")
