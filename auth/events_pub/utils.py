import json
from typing import Any

from confluent_kafka import Producer
from crud.crud_pub_user_event import pub_user_event
from db.session import SessionLocal
from utils.log import get_console_logger

logger = get_console_logger(__name__)
db = SessionLocal()


def delivery_report(err, msg):
    """Called once for each message produced to indicate delivery result.
    Triggered by poll() or flush()."""
    if err is not None:
        pub_user_event.update(db, {"delivered": False, "deliv_fail": True})
        logger.error(f"Message delivery failed: {err}")
    else:
        val = json.loads(msg.value())
        db_obj = pub_user_event.get(db, id=val.get("id"))
        pub_user_event.update(
            db, db_obj=db_obj, obj_in={"delivered": True, "deliv_fail": False}
        )
        logger.info(
            f'Message (ev_id={val.get("id")}) delivered to "{msg.topic()}" '
            f"part=[{msg.partition()}], offs={msg.offset()}"
        )


def send_message(p: Producer, topic: str, msg: Any):
    try:
        logger.info(f"  new_{msg=}")
        p.produce(topic, json.dumps(msg), callback=delivery_report)
        p.flush()
    except Exception as e:
        logger.error(e)
