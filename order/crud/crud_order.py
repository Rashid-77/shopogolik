from typing import Any, Dict, Optional, Union
from uuid import UUID

from crud.base import CRUDBase
from models.order import Order
from schemas.order import OrderCreate, OrderUpdate
from sqlalchemy.orm import Session


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    def get(self, db: Session, uuid: UUID) -> Optional[Order]:
        return db.query(self.model).filter(self.model.uuid == uuid).first()

    def create(self, db: Session, *, obj_in: OrderCreate, user_id) -> Order:
        db_obj = Order(
            uuid=obj_in.uuid,
            userId=user_id,
            goods_reserved=obj_in.goods_reserved,
            money_reserved=obj_in.money_reserved,
            courier_reserved=obj_in.courier_reserved,
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


order = CRUDOrder(Order)
