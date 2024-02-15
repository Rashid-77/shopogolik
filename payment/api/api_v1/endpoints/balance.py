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


@router.post("/deposit", response_model=schemas.Balance)
@REQUEST_TIME_BACKET.labels(endpoint='/balance').time()
def create_deposit(
    bal_in: schemas.BalanceCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create money deposit to in-shop account.
    depos_uuid should be unique for every deposit
    only positive amount is allowed
    """
    logger.info("create_deposit()")
    
    logger.info(f" user_id={current_user.id}, admin={current_user.is_superuser}, "
                f"amount={bal_in.amount}")

    if current_user.id == bal_in.user_id or current_user.is_superuser:
        if bal_in.amount < 0:
            raise HTTPException(status_code=422, detail="Unprocessable Entity.")
        acc = crud.money_account.create(db, 
                                        bal_in.user_id, 
                                        bal_in.depos_uuid, 
                                        bal_in.amount)
        if acc is None:
            raise HTTPException(status_code=422, detail="Unprocessable Entity.")
        return acc
    raise HTTPException(status_code=400, detail="The user doesn't have enough privilege")


@router.post("/withdraw", response_model=schemas.Balance)
@REQUEST_TIME_BACKET.labels(endpoint='/balance').time()
def do_withdraw(
    bal_in: schemas.BalanceWithdraw,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Withdraw money from in-shop account.
    withdraw_uuid should be unique for every withdraw
    only positive amount is allowed
    """
    logger.info("do_withdraw()")
    
    logger.info(f" user_id={current_user.id}, admin={current_user.is_superuser}, "
                f"amount={bal_in.amount}")

    if current_user.id == bal_in.user_id or current_user.is_superuser:
        if bal_in.amount < 0:
            raise HTTPException(status_code=422, detail="Unprocessable Entity.")
        acc = crud.money_account.withdraw(db, 
                                          bal_in.user_id, 
                                          bal_in.withdraw_uuid, 
                                          bal_in.amount)
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
        return acc
    raise HTTPException(status_code=400, detail="The user doesn't have enough privilege")
