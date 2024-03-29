from confluent_kafka import Producer
from crud.crud_pub_user_event import pub_user_event
from db.session import SessionLocal
from events_pub.utils import send_message
from logger import logger
from models.user import User
from schemas.pub_user_event import PubUserEventCreate
from utils.config import get_settings

logger.info("User started")
kafka_url = get_settings().broker_url
logger.info(f"{kafka_url=}")

# TODO check kafka readiness
p = Producer({"bootstrap.servers": kafka_url})
db = SessionLocal()


def publish_user_created(user: User):
    user_msg = {
        "name": "user",
        "state": "new_user",
        "user_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phone": user.phone,
        "disabled": user.disabled,
        "is_superuser": user.is_superuser,
    }
    event = PubUserEventCreate(user_id=user.id, state=user_msg["state"])
    pub_ev = pub_user_event.create(db, obj_in=event)
    user_msg["id"] = pub_ev.id
    send_message(p, "user", user_msg)
