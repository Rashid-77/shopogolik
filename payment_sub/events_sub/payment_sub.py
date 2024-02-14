import json
from decimal import Decimal

from crud.crud_pub_event import pub_event
from crud.crud_sub_event import sub_event
from schemas.sub_event import SubEventCreate
from schemas.pub_event import PubEventCreate
from utils.log import get_console_logger
from db.session import SessionLocal
from events_sub.db_utils import balance_utils

logger = get_console_logger(__name__)
logger.info("Payment_sub started")

db = SessionLocal()


def process_payment(msg):
    ''' 
    Reserve money or cancel reservation
    If message sucessfully processed answer will be sent
    '''
    val = json.loads(msg.value())

    if val.get("name") == "order":
        event_id = val.get("id")
        sub_ev = sub_event.get_by_event_id(db, event_id)
        if sub_ev is not None:
            logger.warn("This is duplicate. Ignored")
            return
        
        order_uuid = val.get("order_uuid")
        sub_ev = sub_event.create(
            db, obj_in=SubEventCreate(event_id=event_id, order_id=order_uuid)
        )
        answer_msg = {
            "name" : "payment",
            "order_uuid": order_uuid, 
            "user_id": val.get("user_id")
        }

        if val.get("state") == "canceling":
            success = balance_utils.cancel_reserved(
                event_id,
                val.get("user_id"),
                order_uuid, 
                answ_msg=answer_msg
            )
            if not success:
                return
            logger.error(f'Reservation for order {order_uuid} canceled')

        elif val.get("state") == "new_order":
            success = balance_utils.reserve_money(
                event_id, 
                val.get("user_id"), 
                order_uuid, 
                amount=Decimal(val.get("to_pay")),
                answ_msg=answer_msg
            )
            if not success and answer_msg['state'] == 'already reserved':
                return
        else:
            return
        
        pub_ev  = pub_event.create(db, obj_in=PubEventCreate(order_id=order_uuid))
        answer_msg["id"] = pub_ev.id
    
        return answer_msg
