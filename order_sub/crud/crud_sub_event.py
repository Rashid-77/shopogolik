from typing import Any, Optional, Dict, Union
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.sub_event import SubProdEvent, SubPaymEvent, SubLogisEvent
from schemas.sub_event import SubEventCreate, SubEventUpdate


class CRUDSubEvent(CRUDBase[SubProdEvent, SubEventCreate, SubEventUpdate]):

    def get_by_event_id(self, db: Session, ev_id: int) -> Optional[SubProdEvent]:
        return db.query(self.model).filter(self.model.event_id == ev_id).first()

    def is_exists(self, db: Session, *, id: int) -> Optional[SubProdEvent]:
        return db.query(SubProdEvent).filter(SubProdEvent.id == id).first()


class CRUDSubEvent(CRUDBase[SubPaymEvent, SubEventCreate, SubEventUpdate]):

    def get_by_event_id(self, db: Session, ev_id: int) -> Optional[SubPaymEvent]:
        return db.query(self.model).filter(self.model.event_id == ev_id).first()

    def is_exists(self, db: Session, *, id: int) -> Optional[SubPaymEvent]:
        return db.query(SubPaymEvent).filter(SubPaymEvent.id == id).first()

sub_prod_event = CRUDSubEvent(SubProdEvent)
sub_paym_event = CRUDSubEvent(SubPaymEvent)
sub_logis_event = CRUDSubEvent(SubLogisEvent)
