from datetime import datetime
from typing import Any, Dict, Optional, Union

from sqlalchemy import and_
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.courier import Courier
from schemas.courier import CourierCreate, CourierUpdate
from logger import logger

class CRUDCourier(CRUDBase[Courier, CourierCreate, CourierUpdate]):
    
    def get_courier_id(self, db: Session, user_id) -> Optional[Courier]:
        return db.query(Courier).filter(Courier.courier_id == user_id).first()

    def get_free(self, db: Session, offset: int, limit: int) -> Optional[Courier]:
        return db.query(Courier) \
                .filter(
                    and_(
                        Courier.from_t == datetime.min, 
                        Courier.to_t == datetime.min,
                        Courier.order_uuid == "",
                        Courier.deliv_addr == "",
                        )
                ).offset(offset).limit(limit).all()

    def create(self, db: Session, *, user_id: int) -> Courier:
        db_obj = Courier(courier_id = user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Courier, obj_in: Union[CourierUpdate, Dict[str, Any]]
    ) -> Courier:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def remove(self, db: Session, *, user_id: int) -> Courier:
        obj = db.query(Courier).filter(Courier.courier_id == user_id).first()
        if obj is None:
            return None
        db.delete(obj)
        db.commit()
        return obj
    

courier = CRUDCourier(Courier)
