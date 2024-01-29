from typing import Any, Optional, Dict, Union
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.pub_event import PubEvent
from schemas.pub_event import PubEventCreate, PubEventUpdate
from logger import logger

class CRUDPubEvent(CRUDBase[PubEvent, PubEventCreate, PubEventUpdate]):

    def get(self, db: Session, id: int) -> Optional[PubEvent]:
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, *, obj_in: PubEventCreate) -> PubEvent:
        db_obj = PubEvent(
            delivered = False,
            deliv_fail = False,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: PubEvent, obj_in: Union[PubEventUpdate, Dict[str, Any]]
    ) -> PubEvent:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def is_exists(self, db: Session, *, id: int) -> Optional[PubEvent]:
        return db.query(PubEvent).filter(PubEvent.id == id).first()


pub_event = CRUDPubEvent(PubEvent)
