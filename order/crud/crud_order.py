from typing import Any, Optional, Dict, Union
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.order import Order
from schemas.order import OrderCreate, OrderUpdate


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):

    def get(self, db: Session, id: int) -> Optional[Order]:
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, *, obj_in: OrderCreate, user_id) -> Order:
        db_obj = Order(
            userId = user_id,
            amount = obj_in.amount,
            shipName = obj_in.shipName,
            shipAddr = obj_in.shipAddr,
            city = obj_in.city,
            state = obj_in.state,
            zip = obj_in.zip,
            country = obj_in.country,
            email = obj_in.email,
            phone = obj_in.phone,
            tax = obj_in.tax,
            shiped = False,
            shipDate = None,
            trackinNumber = ""
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Order, obj_in: Union[OrderUpdate, Dict[str, Any]]
    ) -> Order:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def is_order_exists(self, db: Session, *, id: int) -> Optional[Order]:
        return db.query(Order).filter(Order.id == id).first()


order = CRUDOrder(Order)
