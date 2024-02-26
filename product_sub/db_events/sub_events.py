from typing import Optional

from models.sub_event import SubEvent
from sqlalchemy.orm import Session


class SubEventUtils:
    def get_orders(self, db: Session, order_id: int) -> Optional[SubEvent]:
        return db.query(SubEvent).filter(SubEvent.order_id == order_id).all()


sub_ev_utils = SubEventUtils()
