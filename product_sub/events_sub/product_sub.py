# from decimal import *
import json

from confluent_kafka import Producer, Consumer, KafkaException, KafkaError
from crud.crud_pub_event import pub_event
from crud.crud_sub_event import sub_event
from schemas.sub_event import SubEventCreate
from utils import get_settings
from utils.log import get_console_logger
from db.session import SessionLocal
from events_sub.utils import delivery_report

CONSUMER_GROUP = 'product_group'


logger = get_console_logger(__name__)
logger.info("Product_sub started")

kafka_url = get_settings().broker_url
p = Producer({'bootstrap.servers': kafka_url})
db = SessionLocal()

# In memory stock data for dev
stock = [
    {"rod_id": 0, "amount": 0},
    {"prod_id": 1, "amount": 100},
    {"prod_id": 2, "amount": 50},
]


def how_many_prod(prod_id):
    ''' It returns the number of products in stock '''
    return stock[prod_id].get("amount")


def reserve_prod(prod_id, amount):
    ''' 
    It reserves the number of products in stock
    If products are not enough then returns the number of reserved products
    '''
    amount_now = stock[prod_id].get("amount")
    if amount_now <= 0:
        return 0
    elif amount_now >= amount:
        stock[prod_id]["amount"] -= amount
        return amount
    stock[prod_id]["amount"] = 0
    return amount_now


def dispatch_msgs(msg):
    val = json.loads(msg.value())

    if val.get("name") == "order":
        sub_ev = sub_event.get_by_event_id(db, val.get("id"))
        if sub_ev is not None:
            logger.warn("This is duplicate. Ignored")
            return
        prod_msg = {
            "name" : "product", 
            "order_uuid": val.get("order_uuid"), 
            "reserved": [],
        }
        # TODO here insert event state 1 of buisness logic
        for prod in val.get("products"):
            prod_id, amount = prod.get("prod_id"), prod.get("amount")
            res_amount = reserve_prod(prod_id, amount)
            prod_msg["reserved"].append({"prod_id":prod_id, "amount": res_amount})

        sub_ev = sub_event.create(db, obj_in=SubEventCreate(event_id=val.get("id")))
        # TODO here insert event state 2 of buisness logic
        pub_ev  = pub_event.create(db, obj_in=None)
        prod_msg["id"] = pub_ev.id
        try:
            p.produce('product', json.dumps(prod_msg), callback=delivery_report)
            p.flush()
            # TODO here insert event state 3 of buisness logic
        except Exception as e:
            logger.error(e)


def main_consume_loop():
    logger.info("basic_consume_loop()")
    try:
        c = Consumer({
            'bootstrap.servers': kafka_url,
            'group.id': CONSUMER_GROUP,
            'auto.offset.reset': 'earliest'
        })

        c.subscribe(['order'])
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
    finally:
        # Close down consumer to commit final offsets.
        logger.error('Consumer closed down')
        c.close()
