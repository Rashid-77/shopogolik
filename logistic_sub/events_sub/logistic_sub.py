from decimal import Decimal
import json

from confluent_kafka import Producer, Consumer, KafkaException, KafkaError
from crud.crud_pub_event import pub_event
from crud.crud_sub_event import sub_event
from schemas.sub_event import SubEventCreate
from schemas.pub_event import PubEventCreate
from utils import get_settings
from utils.log import get_console_logger
from db.session import SessionLocal
from events_sub.utils import send_message
from events_sub.db_utils import logistic_utils

CONSUMER_GROUP = 'logistic_group'


logger = get_console_logger(__name__)
logger.info("Logistic_sub started")

kafka_url = get_settings().broker_url
p = Producer({'bootstrap.servers': kafka_url})
db = SessionLocal()


def dispatch_msgs(msg):
    val = json.loads(msg.value())

    if val.get("name") == "order":
        event_id = val.get("id")
        sub_ev = sub_event.get_by_event_id(db, event_id)
        if sub_ev is not None:
            logger.warn("This is duplicate. Ignored")
            return
        
        order_uuid = val.get("order_uuid")
        sub_ev = sub_event.create(
            db, obj_in=SubEventCreate(event_id=event_id, order_id=order_uuid)
        )
        answer_msg = {
            "name" : "logistic",
            "order_uuid": order_uuid, 
            "user_id": val.get("user_id")
        }

        if val.get("state") == "canceling":
            success = logistic_utils.cancel_reserved(
                event_id,
                order_uuid, 
                answ_msg=answer_msg
            )
            if not success:
                return
        elif val.get("state") == "new_order":
            success = logistic_utils.reserve_courier(
                event_id, 
                client_id = val.get("user_id"), 
                order_uuid = order_uuid,
                deliv_time_from = val.get("deliv_t_from"),
                deliv_time_to = val.get("deliv_t_to"),
                deliv_addr = val.get("deliv_addr"),
                answ_msg = answer_msg
            )
            if not success and answer_msg['state'] == 'already reserved':
                return
        else:
            return

        pub_ev  = pub_event.create(db, obj_in=PubEventCreate(order_id=order_uuid))
        answer_msg["id"] = pub_ev.id
        send_message(p, "logistic", answer_msg)


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
