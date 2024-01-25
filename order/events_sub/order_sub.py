import json
import time
import asyncio
from confluent_kafka import Producer, Consumer, KafkaException, KafkaError
import logging 
from utils import get_settings

logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname).1s %(message)s",
        datefmt="%Y.%m.%d %H:%M:%S",
    )
logging.info("Tick started")
logging.info('wait until kafka is started ...')

# kafka_url = 'broker:9092'
kafka_url = get_settings().broker_url
logging.info(f'{kafka_url=}')


async def basic_consume_loop():
    try:
        c = Consumer({
            'bootstrap.servers': kafka_url,
            'group.id': 'prod_group',
            'auto.offset.reset': 'earliest'
        })

        c.subscribe(['order'])
        while True:
            msg = c.poll(1.0)
            # logging.info('polled..')

            if msg is None: continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    logging.error('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                logging.info(f'<--- Received: {msg.value()}')
    finally:
        # Close down consumer to commit final offsets.
        c.close()


async def tick():
    cnt = 10
    while cnt:
        logging.info(f'----- Tick: {cnt}')
        await asyncio.sleep(1)
        cnt -= 1
    logging.info("Tick finished")
