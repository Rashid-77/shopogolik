from typing import Optional
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.balance import Balance
from models.depos_idemp import deposidemp
from schemas.balance import BalanceCreate, BalanceUpdate
from logger import logger


class CRUDBalance(CRUDBase[Balance, BalanceCreate, BalanceUpdate]):

    def get(self, db: Session, id: int) -> Optional[Balance]:
        return db.query(Balance).filter(Balance.id == id).first()

    def get_by_user_id(self, db: Session, *, user_id: int) -> Optional[Balance]:
        return db.query(Balance) \
                .filter(Balance.user_id == user_id) \
                .order_by(Balance.created_at.desc()).first()

    def get_balance(self, db: Session, *, user_id: int) -> Optional[Balance]:
        return db.query(Balance) \
                .filter(Balance.user_id == user_id) \
                .order_by(Balance.created_at.desc()).first()

    def create(
            self, db: Session, user_id: int, depos_uuid: str, amount: float
        ) -> Balance:
        idemp = db.query(deposidemp).filter(deposidemp.uuid == depos_uuid).first()
        if idemp:
            logger.warn(f"idempotency: duplicate {depos_uuid=}")
            return None
        
        account = db.query(Balance) \
                    .filter(Balance.user_id == user_id) \
                    .order_by(Balance.created_at.desc()).first()
        balance = 0 if account is None else account.balance
        new_balance = balance + amount
        if new_balance < 0:
            logger.warn(f"{user_id=}, {depos_uuid=}, New balance < 0 "
                        f"current balance({balance}) + amount({amount}) = {new_balance}")
            return None
        
        db_idemp = deposidemp(uuid=depos_uuid)

        db_bal = Balance(
            user_id = user_id,
            deposidemp = db_idemp,
            balance = new_balance,
            amount = amount,
            deposit = True,
        )
        db.add(db_bal)
        db.commit()
        db.refresh(db_bal)
        return db_bal

    # def update(
    #     self, db: Session, *, db_obj: Balance, obj_in: Union[BalanceUpdate, Dict[str, Any]]
    # ) -> Balance:
    #     if isinstance(obj_in, dict):
    #         update_data = obj_in
    #     else:
    #         update_data = obj_in.model_dump(exclude_unset=True)
    #     return super().update(db, db_obj=db_obj, obj_in=update_data)

    # def update_balance(
    #     self, db: Session, user_id: int, amount: float
    # ) -> Balance:
    #     account = db.query(Balance) \
    #                 .filter(Balance.user_id == user_id) \
    #                 .order_by(Balance.updDate.desc()).first()
    #     new_balance = account.balance + amount
    #     if new_balance < 0:
    #         return None
    #     account.balance = new_balance
    #     if amount < 0:
    #         account.deposit = True
    #     db.add(account)
    #     db.commit()
    #     return account

    def is_exists(self, db: Session, *, user_id: int) -> Optional[Balance]:
        return db.query(Balance).filter(Balance.user_id == user_id).first()


money_account = CRUDBalance(Balance)
