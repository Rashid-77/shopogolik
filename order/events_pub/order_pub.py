import json

from confluent_kafka import Producer, Consumer
from models.order import Order
from logger import logger
from utils import get_settings

logger.info('Product started')
logger.info('wait until kafka is started ...')

kafka_url = get_settings().broker_url

# TODO check kafka readiness
p = Producer({'bootstrap.servers': kafka_url})


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        logger.error(f'Message delivery failed: {err}')
    else:
        logger.info(f'Message delivered to {msg.topic()} [{msg.partition()}], o={msg.offset()}')

# TODO put it in DB
# id for idempotency
order_ev_id: int = 0

import random
def publish_order_created(order: Order):
    '''
    When user submit order, this event publicates then:
    - product service have to reserve goods in warehouse if their quantity is sufficient
    - payment service have to check ballance and reserve money for order
    - logistic service have to check if address is accessible for the courier and
      have to reserve courier at ponted time
    '''
    global order_ev_id
    # TODO change products to the real data from cart
    products = [
        {"prod_id": 1, "amount": random.randint(1, 20)},
        {"prod_id": 2, "amount": random.randint(1, 5)},
    ]
    # order_msg = {"order": order.uuid, "products": products}
    order_msg = {
        "name" : "order",
        "order_uuid": order.uuid.hex, 
        "order_ev_id": order_ev_id, 
        "products": products,
        "to_pay": "13"
    }
    logger.info(f"--> sent msg {order_msg=}")
    try:
        p.produce('order', json.dumps(order_msg), callback=delivery_report)
        p.flush()
        order_ev_id += 1
    except Exception as e:
        logger.error(e)
