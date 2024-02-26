from typing import Any, Dict, List, Optional, Union

from crud.base import CRUDBase
from models.sub_user_event import SubUserEvent
from schemas.sub_user_event import SubUserEventCreate, SubUserEventUpdate
from sqlalchemy.orm import Session


class CRUDSubUserEvent(CRUDBase[SubUserEvent, SubUserEventCreate, SubUserEventUpdate]):
    def get(self, db: Session, id: int) -> Optional[SubUserEvent]:
        return db.query(SubUserEvent).filter(SubUserEvent.id == id).first()

    def get_by_event_id(self, db: Session, ev_id: int) -> Optional[SubUserEvent]:
        return db.query(SubUserEvent).filter(SubUserEvent.event_id == ev_id).first()

    def get_by_user_id(self, db: Session, user_id: int) -> Optional[SubUserEvent]:
        return (
            db.query(SubUserEvent)
            .filter(SubUserEvent.user_id == user_id)
            .order_by(SubUserEvent.created_at.desc())
            .first()
        )

    def get_by_user_id_all(
        self, db: Session, user_id: int
    ) -> Optional[List[SubUserEvent]]:
        return db.query(SubUserEvent).filter(SubUserEvent.user_id == user_id).all()

    def create(self, db: Session, obj_in: SubUserEventCreate) -> SubUserEvent:
        db_obj = SubUserEvent(
            event_id=obj_in.event_id,
            user_id=obj_in.user_id,
            state=obj_in.state,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        db_obj: SubUserEvent,
        obj_in: Union[SubUserEventUpdate, Dict[str, Any]],
    ) -> SubUserEvent:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def is_exists(self, db: Session, *, id: int) -> Optional[SubUserEvent]:
        return db.query(SubUserEvent).filter(SubUserEvent.id == id).first()


sub_user_event = CRUDSubUserEvent(SubUserEvent)
