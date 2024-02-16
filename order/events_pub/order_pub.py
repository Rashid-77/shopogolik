from confluent_kafka import Producer

from crud.crud_pub_event import pub_event
from db.session import SessionLocal
from events_pub.utils import send_message
from logger import logger
from schemas.pub_event import PubEventCreate
from schemas.order_info import OrderInfoCreate
from utils import get_settings

logger.info('Product started')
kafka_url = get_settings().broker_url

# TODO check kafka readiness
p = Producer({'bootstrap.servers': kafka_url})
db = SessionLocal()


def publish_order_created(order: OrderInfoCreate):
    '''
    When user submit order, this event publicates then:
    - product service have to reserve goods in warehouse if their quantity is sufficient
    - payment service have to check ballance and reserve money for order
    - logistic service have to check if address is accessible for the courier and
      have to reserve courier at ponted time
    '''
    order_msg = {
        "name" : "order",
        "order_uuid": order.uuid.hex, 
        "user_id": order.userId,
        "deliv_t_from": order.deliv_t_from.strftime("%Y-%d-%m, %H:%M:%S"),
        "deliv_t_to": order.deliv_t_to.strftime("%Y-%d-%m, %H:%M:%S"),
        "deliv_addr": order.deliv_addr,
        "products": order.products,
        "to_pay": "13",
        "state": "new_order"
    }
    pub_ev  = pub_event.create(db, obj_in=PubEventCreate(order_id=order.uuid.hex))
    order_msg["id"] = pub_ev.id
    send_message(p, "order", order_msg)
