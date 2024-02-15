
import json
from typing import Any, Callable
from confluent_kafka import Producer, Consumer, KafkaException, KafkaError
from db.session import SessionLocal
from utils.log import get_console_logger

logger = get_console_logger(__name__)


class KafkaConsumer:
    def __init__(
            self, 
            kafka_url: str, 
            consumer_group: str, 
            pub_event,
            process_msg: Callable[[Any,], Any],
            listen_topic: str,
            answer_topic: str = None,
            poll_interval: float = 1.0,
        ) -> None:
        self.kafka_url = kafka_url
        self.consumer_group = consumer_group
        self.poll_interval = poll_interval
        self.pub_event = pub_event
        self.process_msg = process_msg
        self.listen_topic = listen_topic
        self.answer_topic = answer_topic
        self.p = Producer({'bootstrap.servers': self.kafka_url})
        self.c = Consumer({
            'bootstrap.servers': self.kafka_url,
            'group.id': self.consumer_group,
            'auto.offset.reset': 'earliest'
        })

    def delivery_report(self, err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        with SessionLocal() as db:
            if err is not None:
                self.pub_event.update(db, {"delivered": False, "deliv_fail": True})
                logger.error(f'Message delivery failed: {err}')
                logger.error(f'  ev_id={{val.get("id")}}')
            else:
                val = json.loads(msg.value())
                db_obj = self.pub_event.get(db, id=val.get('id'))
                self.pub_event.update(db, 
                                db_obj=db_obj, 
                                obj_in={"delivered": True, "deliv_fail": False})
                logger.info(f'Message (ev_id={val.get("id")}) delivered to "{msg.topic()}" '
                            f'part=[{msg.partition()}], offs={msg.offset()}')

    def send_message(self, topic: str, msg: Any):
        if topic is None or topic == "":
            return
        try:
            logger.info(f'  new_{msg=}')
            self.p.produce(topic, json.dumps(msg), callback=self.delivery_report)
            self.p.flush()
        except Exception as e:
            logger.error(e)

    def subscribe(self):
        return self.c.subscribe([self.listen_topic])

    def consumer_poll(self):
        return self.c.poll(self.poll_interval)
        

    def dispatch_msg(self, msg: Any):
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event
                logger.error('%% %s [%d] reached end at offset %d\n' %
                                 (msg.topic(), msg.partition(), msg.offset()))
            elif msg.error():
                raise KafkaException(msg.error())
        else:
            logger.info(f'<--- Received: t={msg.topic()}, p={msg.partition()}, '
                        f'o={msg.offset()}')
            logger.info(f'     msg:{json.loads(msg.value())}')
            answer = self.process_msg(msg)
            if answer:
                self.send_message(self.answer_topic, answer)
