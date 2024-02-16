import json

from crud.crud_pub_user_event import pub_user_event
from crud.crud_sub_user_event import sub_user_event
from crud.crud_user_lim import user
from db.session import SessionLocal
from schemas.sub_user_event import SubUserEventCreate
from schemas.pub_user_event import PubUserEventCreate
from schemas.user_lim import UserCreate
from utils.log import get_console_logger


logger = get_console_logger(__name__)
logger.info("User_sub started")

db = SessionLocal()


def process_user(msg):
    ''' 
    Reserve money or cancel reservation
    If message sucessfully processed answer will be sent
    '''
    val = json.loads(msg.value())

    if val.get("name") == "user":
        event_id = val.get("id")
        sub_ev = sub_user_event.get_by_event_id(db, event_id)
        if sub_ev is not None:
            logger.warn("This is duplicate. Ignored")
            return
        
        user_id = val.get("user_id")
        state = val.get("state")
        sub_ev = sub_user_event.create(
            db, obj_in=SubUserEventCreate(
                event_id=event_id, user_id=user_id, state=state)
        )
        answer_msg = {
            "name" : "payment-user",
            "user_id": user_id
        }

        if state == "new_user":
            u = user.create(db, obj_in=UserCreate(
                user_id = val.get("user_id"),
                username = val.get("username"),
                first_name = val.get("first_name"),
                last_name = val.get("last_name"),
                email = val.get("email"),
                phone = val.get("phone"),
                disabled = val.get("disabled"),
                is_superuser = val.get("is_superuser")
            ))
            if not u:
                return
            answer_msg["state"] = "User created"
            logger.info(f'user id={user_id} created')

        elif state == "update_user":
            # TODO update user
            answer_msg["state"] = "Not implemented"
            logger.warn(f'"update_user" Not implemented')
        else:
            logger.error(f' Unprocessed state = {val.get("state")}')
            return
        
        ev = PubUserEventCreate(user_id=user_id, state=answer_msg["state"])
        pub_ev  = pub_user_event.create(db, obj_in=ev)
        answer_msg["id"] = pub_ev.id
    
        return answer_msg
