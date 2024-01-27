from decimal import *
import json

from confluent_kafka import Producer, Consumer, KafkaException, KafkaError

from db.utils import get_db
from crud import order
from models import Order
from schemas.order import OrderUpdate
from utils import get_settings
from utils.log import get_console_logger
from db.session import SessionLocal

CONSUMER_GROUP = 'order_group'


logger = get_console_logger(__name__)
logger.info("Order_sub started")

kafka_url = get_settings().broker_url
p = Producer({'bootstrap.servers': kafka_url})
# db = get_db()
db = SessionLocal()

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        logger.error(f'Message delivery failed: {err}')
    else:
        logger.info(f'Message delivered to {msg.topic()} [{msg.partition()}]')


prod_events = []

def dispatch_msgs(msg):
    val = json.loads(msg.value())
    prod_ev_id = val.get("prod_ev_id")
    logger.info(f'{prod_ev_id=}, {prod_events=}')

    if prod_ev_id in prod_events:
        logger.warn("This is duplicate. Ignored")
        return
    prod_events.append(val.get("order_ev_id"))

    if val.get("name") == "product":
        at_least_one_reserved = False
        for prod in val.get("reserved"):
            logger.info(f'{prod}')
            if prod.get("amount") > 0:
                at_least_one_reserved = True
                break
        if at_least_one_reserved:
            # set order.goods_reserved to True
            o: Order = order.get(db, val.get("order_uuid"))
            logger.info(f'{o=}')
            upd = {"goods_reserved": True}
            logger.info(f'{upd=}')
            updated = order.update(db, db_obj=o, obj_in=upd)
            logger.info(f'{updated=}')
    elif val.get("name") == "payment":
        pass
    elif val.get("name") == "logistic":
        pass


def main_consume_loop():
    logger.info("basic_consume_loop()")
    try:
        c = Consumer({
            'bootstrap.servers': kafka_url,
            'group.id': CONSUMER_GROUP,
            'auto.offset.reset': 'earliest'
        })

        c.subscribe(['product'])
        while True:
            # TODO change to poll consume to the batch consume in the future
            msg = c.poll(3)

            if msg is None: 
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    logger.error('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                logger.info(f'<--- Received: t={msg.topic()}, p={msg.partition()}, o={msg.offset()}')
                logger.info(f'     msg:{json.loads(msg.value())}')
                dispatch_msgs(msg)
                # logger.info(f'{prod_req=}')
    finally:
        # Close down consumer to commit final offsets.
        logger.error('Consumer closed down')
        c.close()
