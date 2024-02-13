from typing import Any, Dict, Optional, Union
from uuid import UUID
from sqlalchemy import and_
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.notify import Notify
from schemas.notify import NotifyCreate, NotifyUpdate
from logger import logger

class CRUDNotify(CRUDBase[Notify, NotifyCreate, NotifyUpdate]):
    
    def get_by_order_id(self, db: Session, order_uuid: UUID) -> Optional[Notify]:
        return db.query(Notify) \
            .filter(Notify.order_uuid == order_uuid) \
            .order_by(Notify.created_at.desc()) \
            .first()

    def create(self, db: Session, *, obj_in: NotifyCreate) -> Notify:
        db_obj = Notify(
            order_uuid = obj_in.order_uuid,
            client_id = obj_in.client_id,
            msg = obj_in.msg,
            )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Notify, obj_in: Union[NotifyUpdate, Dict[str, Any]]
    ) -> Notify:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def remove(self, db: Session, *, user_id: int) -> Notify:
        obj = db.query(Notify).filter(Notify.courier_id == user_id).first()
        if obj is None:
            return None
        db.delete(obj)
        db.commit()
        return obj
    

notify = CRUDNotify(Notify)
