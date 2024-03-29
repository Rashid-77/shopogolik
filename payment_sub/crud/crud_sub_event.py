from typing import Any, Dict, Optional, Union

from crud.base import CRUDBase
from models.sub_event import SubEvent
from schemas.sub_event import SubEventCreate, SubEventUpdate
from sqlalchemy.orm import Session


class CRUDSubEvent(CRUDBase[SubEvent, SubEventCreate, SubEventUpdate]):
    def get(self, db: Session, id: int) -> Optional[SubEvent]:
        return db.query(SubEvent).filter(SubEvent.id == id).first()

    def get_by_event_id(self, db: Session, ev_id: int) -> Optional[SubEvent]:
        return db.query(SubEvent).filter(SubEvent.event_id == ev_id).first()

    def create(self, db: Session, obj_in: SubEventCreate) -> SubEvent:
        db_obj = SubEvent(
            event_id=obj_in.event_id,
            order_id=obj_in.order_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: SubEvent,
        obj_in: Union[SubEventUpdate, Dict[str, Any]],
    ) -> SubEvent:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def is_exists(self, db: Session, *, id: int) -> Optional[SubEvent]:
        return db.query(SubEvent).filter(SubEvent.id == id).first()


sub_event = CRUDSubEvent(SubEvent)
