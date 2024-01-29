from decimal import *
import json

from confluent_kafka import Producer, Consumer, KafkaException, KafkaError
from crud.crud_pub_event import pub_event
from crud.crud_sub_event import sub_event
from schemas.sub_event import SubEventCreate
from crud import order
from models import Order
from schemas.order import OrderUpdate
from utils import get_settings
from utils.log import get_console_logger
from db.session import SessionLocal
from events_sub.utils import send_message

CONSUMER_GROUP = 'order_group'


logger = get_console_logger(__name__)
logger.info("Order_sub started")

kafka_url = get_settings().broker_url
p = Producer({'bootstrap.servers': kafka_url})
db = SessionLocal()


def dispatch_msgs(msg):
    val = json.loads(msg.value())

    sub_ev = sub_event.get_by_event_id(db, val.get("id"))
    if sub_ev is not None:
        logger.warn("This is duplicate. Ignored")
        return
    sub_ev = sub_event.create(db, obj_in=SubEventCreate(event_id=val.get("id")))
    # TODO here insert event state 1 of buisness logic

    if val.get("name") == "product":
        at_least_one_reserved = False
        for prod in val.get("reserved", []):
            if prod.get("amount") > 0:
                at_least_one_reserved = True
                break
        o: Order = order.get(db, val.get("order_uuid"))
        if at_least_one_reserved:
            order.update(db, db_obj=o, obj_in={"goods_reserved": True})
            logger.info(f'at least one good reserved')
        else:
            order.update(db, db_obj=o, obj_in={"goods_fail": False})
            # cancel order
            pub_ev  = pub_event.create(db, obj_in=None)
            cancel_order = {
                "name" : "order",
                "order_uuid": val.get("order_uuid"),
                "canceled": True,
                "id": pub_ev.id
            }
            send_message(p, 'order', cancel_order)
            
        # TODO here insert event state 2 of buisness logic
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
            msg = c.poll(0.5)

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
