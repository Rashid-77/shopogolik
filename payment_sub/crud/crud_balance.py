from typing import Optional

from crud.base import CRUDBase
from models.balance import Balance
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

    def is_exists(self, db: Session, *, user_id: int) -> Optional[Balance]:
        return db.query(Balance).filter(Balance.user_id == user_id).first()


money_account = CRUDBalance(Balance)
