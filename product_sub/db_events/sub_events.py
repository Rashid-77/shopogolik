from typing import Any, Optional, Dict, Union
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.sub_event import SubEvent
from schemas.sub_event import SubEventCreate, SubEventUpdate


class SubEventUtils():
    def get_orders(self, db: Session, order_id: int) -> Optional[SubEvent]:
        return db.query(SubEvent).filter(SubEvent.order_id == order_id).all()



sub_ev_utils = SubEventUtils()