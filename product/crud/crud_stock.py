from typing import Any, Dict, Optional, Union

from crud.base import CRUDBase
from models.stock import Stock
from schemas.stock import StockCreate, StockUpdate
from sqlalchemy.orm import Session


class CRUDStock(CRUDBase[Stock, StockCreate, StockUpdate]):
    def get(self, db: Session, id: int) -> Optional[Stock]:
        return db.query(Stock).filter(Stock.id == id).first()

    def get_by_prod_id(self, db: Session, prod_id: int) -> Optional[Stock]:
        return db.query(Stock).filter(Stock.prod_id == prod_id).first()

    def create(self, db: Session, *, obj_in: StockCreate) -> Stock:
        db_obj = Stock(
            prod_id=obj_in.prod_id,
            amount=obj_in.amount,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Stock, obj_in: Union[StockUpdate, Dict[str, Any]]
    ) -> Stock:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def is_prod_id_exists(self, db: Session, *, prod_id: str) -> Optional[Stock]:
        return db.query(Stock).filter(Stock.prod_id == prod_id).first()


stock = CRUDStock(Stock)
