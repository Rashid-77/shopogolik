from typing import Optional

from crud.base import CRUDBase
from logger import logger
from models.balance import Balance
from models.depos_idemp import deposidemp
from schemas.balance import BalanceCreate, BalanceUpdate
from sqlalchemy.orm import Session


class CRUDBalance(CRUDBase[Balance, BalanceCreate, BalanceUpdate]):
    def get(self, db: Session, id: int) -> Optional[Balance]:
        return db.query(Balance).filter(Balance.id == id).first()

    def get_by_user_id(self, db: Session, *, user_id: int) -> Optional[Balance]:
        return (
            db.query(Balance)
            .filter(Balance.user_id == user_id)
            .order_by(Balance.created_at.desc())
            .first()
        )

    def get_balance(self, db: Session, *, user_id: int) -> Optional[Balance]:
        return (
            db.query(Balance)
            .filter(Balance.user_id == user_id)
            .order_by(Balance.created_at.desc())
            .first()
        )

    def create(
        self, db: Session, user_id: int, depos_uuid: str, amount: float
    ) -> Balance:
        idemp = db.query(deposidemp).filter(deposidemp.uuid == depos_uuid).first()
        if idemp:
            logger.warn(f"idempotency: duplicate {depos_uuid=}")
            return None

        account = (
            db.query(Balance)
            .filter(Balance.user_id == user_id)
            .order_by(Balance.created_at.desc())
            .first()
        )
        balance = 0 if account is None else account.balance
        new_balance = balance + amount
        if new_balance < 0:
            logger.warn(
                f"{user_id=}, {depos_uuid=}, New balance < 0 !!! "
                f"current balance({balance}) + amount({amount}) = {new_balance}"
            )
            return None

        db_idemp = deposidemp(uuid=depos_uuid)

        db_bal = Balance(
            user_id=user_id,
            deposidemp=db_idemp,
            balance=new_balance,
            amount=amount,
            deposit=True,
            success=True,
        )
        db.add(db_bal)
        db.commit()
        db.refresh(db_bal)
        return db_bal

    def withdraw(
        self, db: Session, user_id: int, withdraw_uuid: str, amount: float
    ) -> Balance:
        if db.query(deposidemp).filter(deposidemp.uuid == withdraw_uuid).first():
            logger.warn(f"idempotency: duplicate {withdraw_uuid=}")
            return None

        account = (
            db.query(Balance)
            .filter(Balance.user_id == user_id)
            .order_by(Balance.created_at.desc())
            .first()
        )
        balance = 0 if account is None else account.balance
        new_balance = balance - amount
        if new_balance < 0:
            logger.warn(
                f"{user_id=}, {withdraw_uuid=}, New balance < 0 !!! "
                f"current balance({balance}) - amount({amount}) = {new_balance}"
            )
            return None

        db_idemp = deposidemp(uuid=withdraw_uuid)

        db_bal = Balance(
            user_id=user_id,
            deposidemp=db_idemp,
            balance=new_balance,
            amount=amount,
            withdraw=True,
            success=True,
        )
        db.add(db_bal)
        db.commit()
        db.refresh(db_bal)
        return db_bal

    def is_exists(self, db: Session, *, user_id: int) -> Optional[Balance]:
        return db.query(Balance).filter(Balance.user_id == user_id).first()


money_account = CRUDBalance(Balance)
