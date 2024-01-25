import json
import time

from confluent_kafka import Producer, Consumer
from schemas import OrderInDBBase
from models.order import Order
from logger import logger
from utils import get_settings

logger.info('Product started')
logger.info('wait until kafka is started ...')

# kafka_url = 'broker:9092'
kafka_url = get_settings().broker_url
logger.info(f'{kafka_url=}')

# TODO check kafka readiness
p = Producer({'bootstrap.servers': kafka_url})


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        logger.error(f'Message delivery failed: {err}')
    else:
        logger.info(f'Message delivered to {msg.topic()} [{msg.partition()}]')


async def order_created(order: Order):
    # TODO change products to the real data from cart
    products = [
        {"prod_id": 1, "amount": 1},
        {"prod_id": 2, "amount": 1},
    ]
    # order_msg = {"order": order.uuid, "products": products}
    order_msg = {"order": order.id, "products": products}
    logger.info(f"--> sent msg {order_msg=}")
    try:
        p.poll(0)
        p.produce('order', json.dumps(order_msg), callback=delivery_report)
    except Exception as e:
        logger.error(e)
