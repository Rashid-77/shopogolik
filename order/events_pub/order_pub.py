import json
import random

from confluent_kafka import Producer
from models.order import Order
from crud.crud_pub_event import pub_event
from logger import logger
from utils import get_settings
from db.session import SessionLocal
from events_pub.utils import send_message

logger.info('Product started')
kafka_url = get_settings().broker_url

# TODO check kafka readiness
p = Producer({'bootstrap.servers': kafka_url})
db = SessionLocal()


def publish_order_created(order: Order):
    '''
    When user submit order, this event publicates then:
    - product service have to reserve goods in warehouse if their quantity is sufficient
    - payment service have to check ballance and reserve money for order
    - logistic service have to check if address is accessible for the courier and
      have to reserve courier at ponted time
    '''
    # TODO change products to the real data from cart
    products = [
        {"prod_id": 1, "amount": random.randint(1, 20)},
        {"prod_id": 2, "amount": random.randint(1, 5)},
    ]
    deliv_addr = "Some addres"  # TODO get it from db table
    order_msg = {
        "name" : "order",
        "order_uuid": order.uuid.hex, 
        "user_id": order.userId,
        "deliv_t_from": "2024-03-01 10:00:00",
        "deliv_t_to": "2024-03-01 12:00:00",
        "deliv_addr": deliv_addr,
        "products": products,
        "to_pay": "13"
    }
    pub_ev  = pub_event.create(db, obj_in=None)
    order_msg["id"] = pub_ev.id
    send_message(p, "order", order_msg)
