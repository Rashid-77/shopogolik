# from decimal import *
import json


from confluent_kafka import Producer, Consumer, KafkaException, KafkaError
from crud.crud_pub_event import pub_event
from crud.crud_sub_event import sub_event
from crud.reserve_log import reserve_log
from db_events.stock import stock_utils, prod_reserve_msg
from db.session import SessionLocal
from events_sub.utils import send_message
from models.reserve_log import ProdReserveState
from schemas.sub_event import SubEventCreate
from schemas.pub_event import PubEventCreate
from schemas.reserve_log import ReserveCreate
from utils import get_settings
from utils.log import get_console_logger

CONSUMER_GROUP = 'product_group'


logger = get_console_logger(__name__)
logger.info("Product_sub started")

kafka_url = get_settings().broker_url
p = Producer({'bootstrap.servers': kafka_url})
db = SessionLocal()


def dispatch_msgs(msg):
    global reserve_state
    val = json.loads(msg.value())

    if val.get("name") == "order":
        sub_ev = sub_event.get_by_event_id(db, val.get("id"))
        if sub_ev is not None:
            logger.warn("This is duplicate. Ignored")
            return
        order_uuid = val.get("order_uuid")
        sub_ev = sub_event.create(db, obj_in=SubEventCreate(event_id=val.get("id"), 
                                                            order_id=order_uuid))
        
        if val.get("canceled"):
            ''' cancel goods reservation here for order_uuid... '''
            logger.error(f'Reservation for order {val.get("order_uuid")} canceled')
            reserve_log.create_cancel_if_not_exists(
                order_uuid,
                obj_in=ReserveCreate(
                    order_event_id=val.get("id"),
                    order_id=order_uuid,
                    cancel=True,
                    state=ProdReserveState.EVENT_COMMIT,
                )
            )
            stock_utils.cancel_reserved(order_uuid)
            # reserve_log.update()
            return
        
        answ_msg = {
            "name" : "product", 
            "order_uuid": order_uuid, 
            "reserved": [],
        }
        logger.info(f' id={val.get("id")} , order_uuid={order_uuid}')
        cnt_full, cnt_fail = 0, 0
        
        cnt_full, cnt_fail  = stock_utils.reserve_product(
            val.get("id"),
            order_uuid, 
            val.get("products", []),
            answ_msg
        )
        
        if cnt_full == len(val.get("products")):
            answ_msg["state"] = prod_reserve_msg(ProdReserveState.RESERVED)
        elif cnt_fail == len(val.get("products")):
            answ_msg["state"] = prod_reserve_msg(ProdReserveState.OUT_OF_STOCK)
        else:
            answ_msg["state"] = prod_reserve_msg(ProdReserveState.PARTIALLY)

        sub_ev = sub_event.update(db, db_obj=sub_ev, obj_in=SubEventCreate(
                event_id = val.get("id"), 
                order_id = val.get("order_uuid")
            )
        )
        pub_ev  = pub_event.create(db, obj_in=PubEventCreate(order_id=val.get("order_uuid")))
        answ_msg["id"] = pub_ev.id
        send_message(p, "product", answ_msg)


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
