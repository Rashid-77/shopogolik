from decimal import *
import json

from confluent_kafka import Producer, Consumer, KafkaException, KafkaError
from crud.crud_pub_event import pub_event
from crud.crud_sub_event import sub_prod_event, sub_paym_event, sub_logis_event
from schemas.sub_event import SubEventCreate
from schemas.pub_event import PubEventCreate
from crud import order
from models import Order
from utils import get_settings
from utils.log import get_console_logger
from db.session import SessionLocal
from events_sub.utils import send_message

CONSUMER_GROUP = 'order_group'
POLL_WAIT = 0.3

logger = get_console_logger(__name__)
logger.info("Order_sub started")

kafka_url = get_settings().broker_url
p = Producer({'bootstrap.servers': kafka_url})
db = SessionLocal()


def dispatch_msgs(msg):
    val = json.loads(msg.value())
    order_uuid = val.get("order_uuid")
    event_id = val.get("id")
    cancel_order = False

    if val.get("name") == "product":
        sub_ev = sub_prod_event.get_by_event_id(db, event_id)
        if sub_ev is not None:
            logger.warn(f"This is duplicate prod msg ev_id={event_id}. Ignored")
            return
        
        sub_ev = sub_prod_event.create(db, obj_in=SubEventCreate(
                event_id=event_id,
                order_id=order_uuid
            )
        )
        at_least_one_reserved = False
        for prod in val.get("reserved", []):
            if prod.get("amount", 0) > 0:
                at_least_one_reserved = True
                break
        o: Order = order.get(db, order_uuid)
        if at_least_one_reserved:
            o =order.update(db, db_obj=o, obj_in={"goods_reserved": True})
            logger.info(f' {val.get("state")}')
        elif val.get("canceled"):
            o =order.update(db, db_obj=o, obj_in={"goods_reserved": False})
            logger.info(f' {val.get("state")}')
        else:
            cancel_order = True
            o =order.update(db, db_obj=o, obj_in={"goods_fail": True})
            logger.info(f'All goods in the order are out of stock')

    elif val.get("name") == "payment":
        sub_ev = sub_paym_event.get_by_event_id(db, event_id)
        if sub_ev is not None:
            logger.warn(f"This is duplicate paym msg ev_id={event_id}. Ignored")
            return

        sub_ev = sub_paym_event.create(db, obj_in=SubEventCreate(
                event_id=event_id, 
                order_id=order_uuid
            )
        )
        o: Order = order.get(db, order_uuid)
        if val.get("reserved"):
            o =order.update(db, db_obj=o, obj_in={"money_reserved": True})
            logger.info(f'Money reserved')
        elif val.get("canceled"):
            o =order.update(db, db_obj=o, obj_in={"money_reserved": False})
            logger.info(f' {val.get("state")}')
        else:
            cancel_order = True
            o =order.update(db, db_obj=o, obj_in={"money_fail": True})
            logger.info(f'Balance is insufficient')

    elif val.get("name") == "logistic":
        sub_ev = sub_logis_event.get_by_event_id(db, event_id)
        if sub_ev is not None:
            logger.warn(f"This is duplicate logistic msg ev_id={event_id}. Ignored")
            return
        sub_ev = sub_logis_event.create(db, obj_in=SubEventCreate(
                event_id=event_id,
                order_id=order_uuid
            )
        )
        o: Order = order.get(db, order_uuid)
        if val.get("reserved"):
            o =order.update(db, db_obj=o, obj_in={"courier_reserved": True})
            logger.info(f'Courier reserved')
        elif val.get("canceled"):
            o =order.update(db, db_obj=o, obj_in={"courier_reserved": False})
            logger.info(f'Courier is canceled')
        else:
            cancel_order = True
            o = order.update(db, db_obj=o, obj_in={"courier_fail": True})
            logger.info(f'There is no available courier')

    if cancel_order:
        pub_ev  = pub_event.create(db, obj_in=PubEventCreate(order_id=order_uuid))
        cancel_order = {
            "name" : "order",
            "user_id": val.get("user_id"),
            "order_uuid": order_uuid,
            "state": "canceling",
            "id": pub_ev.id
        }
        send_message(p, 'order', cancel_order)
    elif o.goods_reserved and o.money_reserved and o.courier_reserved \
        and not o.reserv_user_canceled:
        pub_ev  = pub_event.create(db, obj_in=PubEventCreate(order_id=order_uuid))
        rdy_to_ship = {
            "name" : "order",
            "user_id": val.get("user_id"),
            "order_uuid": order_uuid,
            "state": "rdy_to_ship",
            "id": pub_ev.id
        }
        send_message(p, 'order', rdy_to_ship)


def process_pool(msg):
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            # End of partition event
            logger.error('%% %s [%d] reached end at offset %d\n' %
                             (msg.topic(), msg.partition(), msg.offset()))
        elif msg.error():
            raise KafkaException(msg.error())
    else:
        logger.info(f'')    # gap in log for readability
        logger.info(f'<--- Received: t={msg.topic()}, p={msg.partition()}, o={msg.offset()}')
        logger.info(f'     msg:{json.loads(msg.value())}')
        dispatch_msgs(msg)


def main_consume_loop():
    logger.info("basic_consume_loop()")
    try:
        c_prod = Consumer({
            'bootstrap.servers': kafka_url,
            'group.id': CONSUMER_GROUP,
            'auto.offset.reset': 'earliest'
        })
        c_paym = Consumer({
            'bootstrap.servers': kafka_url,
            'group.id': CONSUMER_GROUP,
            'auto.offset.reset': 'earliest'
        })
        c_logis = Consumer({
            'bootstrap.servers': kafka_url,
            'group.id': CONSUMER_GROUP,
            'auto.offset.reset': 'earliest'
        })

        c_prod.subscribe(['product'])
        c_paym.subscribe(['payment'])
        c_logis.subscribe(['logistic'])
        while True:
            # TODO change to poll consume to the batch consume in the future
            msg = c_prod.poll(POLL_WAIT)
            if msg is not None: 
                process_pool(msg)
            
            msg = c_paym.poll(POLL_WAIT)
            if msg is not None:
                process_pool(msg)

            msg = c_logis.poll(POLL_WAIT)
            if msg is not None:
                process_pool(msg)
    finally:
        # Close down consumer to commit final offsets.
        logger.error('Consumers closed down')
        c_prod.close()
        c_paym.close()
