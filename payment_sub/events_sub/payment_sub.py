from decimal import *
import json

from confluent_kafka import Producer, Consumer, KafkaException, KafkaError
from crud.crud_pub_event import pub_event
from crud.crud_sub_event import sub_event
from schemas.sub_event import SubEventCreate
from utils import get_settings
from utils.log import get_console_logger
from db.session import SessionLocal
from events_sub.utils import send_message

CONSUMER_GROUP = 'payment_group'


logger = get_console_logger(__name__)
logger.info("Product_sub started")

kafka_url = get_settings().broker_url
p = Producer({'bootstrap.servers': kafka_url})
db = SessionLocal()

# In memory user balance for dev
balance = [
    {"user_id": 0, "amount": 30, "reserved": Decimal(0)},
    {"user_id": 1, "amount": 30, "reserved": Decimal(0)},
    {"user_id": 2, "amount": 50, "reserved": Decimal(0)},
]

def get_balance(user_id):
    return Decimal(balance[user_id]["amount"])


def reserve_balance(user_id, amount):
    balance[user_id]["amount"] -= amount
    balance[user_id]["reserved"] = amount
    return balance[user_id]["amount"]


def withdraw_money(user_id):
    balance[user_id]["reserved"] = 0
    return balance[user_id]["amount"]


def dispatch_msgs(msg):
    val = json.loads(msg.value())

    if val.get("name") == "order":
        sub_ev = sub_event.get_by_event_id(db, val.get("id"))
        if sub_ev is not None:
            logger.warn("This is duplicate. Ignored")
            return
        
        if val.get("canceled"):
            ''' cancel money reservation here for order_uuid... '''
            logger.error(f'Reservation for order {val.get("order_uuid")} canceled')
            return
        
        answer_msg = {
            "name" : "payment",
            "order_uuid": val.get("order_uuid"), 
            "reserved": False,
        }
        # TODO here insert event state 1 of buisness logic
        if val.get("user_id") is not None and val.get("to_pay") is not None:
            # Check if there are enough funds
            if get_balance(val.get("user_id")) >= Decimal(val.get("to_pay")):
                reserve_balance(val.get("user_id"), Decimal(val.get("to_pay")))
                answer_msg["reserved"] = True
        logger.info(f' user balance={get_balance(val.get("user_id"))}')
        sub_ev = sub_event.create(db, obj_in=SubEventCreate(event_id=val.get("id")))
        # TODO here insert event state 2 of buisness logic
        pub_ev  = pub_event.create(db, obj_in=None)
        answer_msg["id"] = pub_ev.id
        send_message(p, "payment", answer_msg)


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
