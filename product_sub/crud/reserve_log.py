from typing import Any, Optional, Dict, Union
from sqlalchemy import and_
from sqlalchemy.orm import Session

from db.session import SessionLocal
from crud.base import CRUDBase
from models.reserve_log import Reserve
from schemas.reserve_log import ReserveCreate, ReserveUpdate

class CRUDReserve(CRUDBase[Reserve, ReserveCreate, ReserveUpdate]):

    def get(self, db: Session, id: int) -> Optional[Reserve]:
        return db.query(Reserve).filter(Reserve.id == id).first()

    def get_by_order_id(self, db: Session, order_id) -> Optional[Reserve]:
        return db.query(Reserve).filter(Reserve.order_id == order_id).all()

    def create(self, db: Session, *, obj_in: ReserveCreate) -> Reserve:
        db_obj = Reserve(
            order_event_id = obj_in.order_event_id,
            order_id = obj_in.order_id,
            prod_id = obj_in.prod_id,
            to_reserve = obj_in.to_reserve,
            cancel = obj_in.cancel,
            state = obj_in.state,
            amount_processed = obj_in.amount_processed
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_cancel_if_not_exists(self, order_id, obj_in: ReserveCreate) -> Reserve:
        with SessionLocal() as session:
            cancel_cmd = session.query(Reserve) \
                                .filter(
                                    and_(
                                        Reserve.order_id==order_id, 
                                        Reserve.cancel==True
                                        )).all()
            if cancel_cmd:
                return
            db_obj = Reserve(
                order_event_id = obj_in.order_event_id,
                order_id = obj_in.order_id,
                prod_id = obj_in.prod_id,
                to_reserve = obj_in.to_reserve,
                cancel = obj_in.cancel,
                state = obj_in.state,
                amount_processed = obj_in.amount_processed
            )
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Reserve, obj_in: Union[ReserveUpdate, Dict[str, Any]]
    ) -> Reserve:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def is_prod_id_exists(self, db: Session, *, prod_id: str) -> Optional[Reserve]:
        return db.query(Reserve).filter(Reserve.prod_id == prod_id).first()


reserve_log = CRUDReserve(Reserve)
