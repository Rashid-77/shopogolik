import json

from crud.crud_pub_event import pub_event
from crud.crud_sub_event import sub_event
from crud.crud_notify import notify
from crud.crud_user_lim import user
from db.session import SessionLocal
from models.notify import Notify
from schemas.sub_event import SubEventCreate
from schemas.pub_event import PubEventCreate
from utils.log import get_console_logger







logger = get_console_logger(__name__)
logger.info("Notify_sub started")

db = SessionLocal()




def process_notify(msg):
    val = json.loads(msg.value())

    if val.get("name") == "order":
        event_id = val.get("id")
        sub_ev = sub_event.get_by_event_id(db, event_id)
        if sub_ev is not None:
            logger.warn("This is duplicate. Ignored")
            return
        
        order_uuid = val.get("order_uuid")
        user_id = val.get("user_id")
        sub_ev = sub_event.create(
            db, obj_in=SubEventCreate(event_id=event_id, order_id=order_uuid)
        )
        answer_msg = {
            "name" : "notify",
            "order_uuid": order_uuid, 
            "user_id": user_id
        }
        if val.get("state") == "canceling":
            u = user.get_by_user_id(db, user_id=user_id)
            customer = u.username if u else "?"
            reason = val.get("reason")
            if reason == "balance is insufficient":
                MSG_ORDER_CANCELED = f'Dear customer {customer.capitalize()}, your order '\
                                    f'canceled due your balance is insufficient.'
            else:
                MSG_ORDER_CANCELED = f'Dear customer {customer.capitalize()}, your order '\
                                f'canceled due {reason}. You will receive your money back.'
            n = notify.create(
                db, 
                obj_in=Notify(
                    order_uuid=order_uuid,
                    client_id = user_id,
                    msg = MSG_ORDER_CANCELED
                    )
                )
            answer_msg["msg"] = "order canceling email sent"
        elif val.get("state") == "rdy_to_ship":
            u = user.get_by_user_id(db, user_id=user_id)
            customer = u.username if u else "?"
            MSG_ORDER_PAID = f'Dear customer {customer.capitalize()}, you just have paid your order. '\
                            f'Your goods will be delivered by our couriers.'
            n = notify.create(
                db, 
                obj_in=Notify(
                    order_uuid=order_uuid,
                    client_id = user_id,
                    msg = MSG_ORDER_PAID
                    )
                )
            answer_msg["msg"] = "order ready to ship email sent"
        else:
            return
        
        pub_ev  = pub_event.create(db, obj_in=PubEventCreate(order_id=order_uuid))
        answer_msg["id"] = pub_ev.id
        
        return answer_msg
        # send_message(p, "notify", answer_msg)
