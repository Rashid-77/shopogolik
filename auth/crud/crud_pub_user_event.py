from typing import Any, Optional, Dict, Union, List
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.pub_user_event import PubUserEvent
from schemas.pub_user_event import PubUserEventCreate, PubUserEventUpdate


class CRUDPubUserEvent(CRUDBase[PubUserEvent, PubUserEventCreate, PubUserEventUpdate]):

    def get(self, db: Session, id: int) -> Optional[PubUserEvent]:
        return db.query(PubUserEvent).filter(PubUserEvent.id == id).first()

    def get_by_user_id(self, db: Session, user_id: int) -> Optional[PubUserEvent]:
        return db.query(PubUserEvent) \
                .filter(PubUserEvent.user_id == user_id) \
                .order_by(PubUserEvent.created_at.desc()).first()

    def get_by_user_id_all(self, db: Session, user_id: int) -> Optional[List[PubUserEvent]]:
        return db.query(PubUserEvent).filter(PubUserEvent.user_id == user_id).all()

    def create(self, db: Session, *, obj_in: PubUserEventCreate) -> PubUserEvent:
        db_obj = PubUserEvent(
            user_id = obj_in.user_id,
            state = obj_in.state,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, 
        db: Session, 
        *, 
        db_obj: PubUserEvent, 
        obj_in: Union[PubUserEventUpdate, Dict[str, Any]]
    ) -> PubUserEvent:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def is_exists(self, db: Session, *, id: int) -> Optional[PubUserEvent]:
        return db.query(PubUserEvent).filter(PubUserEvent.id == id).first()


pub_event = CRUDPubUserEvent(PubUserEvent)
