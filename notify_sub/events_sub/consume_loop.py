from crud.crud_pub_event import pub_event
from crud.crud_pub_user_event import pub_user_event
from events_sub.consumer import KafkaConsumer
from events_sub.notify_sub import process_notify
from events_sub.user_sub import process_user
from utils.config import get_settings
from utils.log import get_console_logger


logger = get_console_logger(__name__)
logger.info("main_consume_loop started")

CONSUMER_GROUP = 'notify_group'

def main_consume_loop():
    
    try:
        notify_kafka = KafkaConsumer(
            kafka_url=get_settings().broker_url,
            consumer_group=CONSUMER_GROUP,
            listen_topic = 'order',
            answer_topic = 'notify',
            poll_interval=0.5,
            pub_event=pub_event,
            process_msg = process_notify
            )
        user_kafka = KafkaConsumer(
            kafka_url=get_settings().broker_url,
            consumer_group=CONSUMER_GROUP,
            listen_topic = 'user',
            answer_topic = 'notify-user',
            poll_interval=0.5,
            pub_event=pub_user_event,
            process_msg = process_user
            )
        
        notify_kafka.subscribe()
        user_kafka.subscribe()
        
        while True:
            # TODO change poll consume to the batch consume in the future
            msg = notify_kafka.consumer_poll()
            if msg:
                logger.debug(' notify_kafka')
                notify_kafka.dispatch_msg(msg)

            msg = user_kafka.consumer_poll()
            if msg:
                logger.debug(' user_kafka')
                user_kafka.dispatch_msg(msg)
    finally:
        # Close down consumers to commit final offsets.
        notify_kafka.c.close()
        user_kafka.c.close()
        logger.error('Consumers were closed down')
