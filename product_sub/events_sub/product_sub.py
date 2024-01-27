from decimal import *
import json

from confluent_kafka import Producer, Consumer, KafkaException, KafkaError
from utils import get_settings
from utils.log import get_console_logger

PRODUCT_GROUP = 'product_group'


logger = get_console_logger(__name__)
logger.info("Product started")

kafka_url = get_settings().broker_url
p = Producer({'bootstrap.servers': kafka_url})

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


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        logger.error(f'Message delivery failed: {err}')
    else:
        logger.info(f'Message delivered to {msg.topic()} [{msg.partition()}]')


# TODO put it in DB
# id for idempotency
prod_ev_id: int = 0
order_events = []


def dispatch_msgs(msg):
    global prod_ev_id
    val = json.loads(msg.value())
    order_ev_id = val.get("order_ev_id")
    # logger.info(f'{order_ev_id=}, {prod_req=}')

    if order_ev_id in order_events:
        logger.warn("This is duplicate. Ignored")
        return
    order_events.append(val.get("order_ev_id"))

    if val.get("name") == "order":
        prod_msg = {
            "name" : "product", 
            "order_uuid": val.get("order_uuid"), 
            "reserved": [],
            "prod_ev_id": prod_ev_id, 
        }
        for prod in val.get("products"):
            prod_id, amount = prod.get("prod_id"), prod.get("amount")
            # logger.info(f'before reserve: {prod_id=}, {amount=}, Stock: {stock[prod_id].get("amount")}')
            res_amount = reserve_prod(prod_id, amount)
            prod_msg["reserved"].append({"prod_id":prod_id, "amount": res_amount})
            # logger.info(f'after  reserve: {prod_id=}, {res_amount=}, Stock: {stock[prod_id].get("amount")}')
        
        try:
            logger.info(f'  new_{prod_msg=}')
            p.produce('product', json.dumps(prod_msg), callback=delivery_report)
            p.flush()
            prod_ev_id += 1
        except Exception as e:
            logger.error(e)


def main_consume_loop():
    logger.info("basic_consume_loop()")
    try:
        c = Consumer({
            'bootstrap.servers': kafka_url,
            'group.id': PRODUCT_GROUP,
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
