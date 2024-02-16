from typing import Any, Optional, Dict, Union
from uuid import UUID
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.order import Order
from schemas.order import OrderCreate, OrderUpdate


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):

    def get(self, db: Session, uuid: UUID) -> Optional[Order]:
        return db.query(self.model).filter(self.model.uuid == uuid).first()

    def create(self, db: Session, *, obj_in: OrderCreate, user_id) -> Order:
        db_obj = Order(
            uuid = obj_in.uuid,
            userId = user_id,
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

    def is_order_exists(self, db: Session, *, uuid: UUID) -> Optional[Order]:
        return db.query(Order).filter(Order.uuid == uuid).first()

    def is_canceling(self, db: Session, order_uuid) -> bool:
        res = db.query(Order).filter(Order.uuid == order_uuid) \
            .filter(or_(
                Order.goods_fail == True,
                Order.money_fail == True,
                Order.courier_fail == True,
                Order.reserv_user_canceled == True,
                )
            ) \
            .first()
        return True if res else False


order = CRUDOrder(Order)
