from datetime import datetime
from typing import Optional

from db.session import SessionLocal
from logger import logger
from models.courier import Courier
from sqlalchemy import and_


class LogisticUtils:
    def reserve_courier(
        self,
        event_id: int,
        client_id: int,
        order_uuid: str,
        deliv_time_from: datetime,
        deliv_time_to: datetime,
        deliv_addr: str,
        answ_msg: dict,
    ):
        """
        It reserves the courier from courier table
        """
        logger.info("reserve_courier()")
        with SessionLocal() as session:
            cu = session.query(Courier).filter(Courier.order_uuid == order_uuid).all()
            if len(cu):
                answ_msg["reserved"] = False
                answ_msg["state"] = "already reserved"
                logger.info(f"Courier for the order {order_uuid}) already reserved")
                return False

            c = (
                session.query(Courier)
                .filter(
                    and_(
                        Courier.from_t == datetime.min,
                        Courier.to_t == datetime.min,
                        Courier.order_uuid == "",
                        Courier.deliv_addr == "",
                    )
                )
                .first()
            )

            if c is None:
                answ_msg["reserved"] = False
                answ_msg["state"] = "There is no available couriers"
                logger.info("There is no available couriers")
                return False

            c.reserve_uuid = (event_id,)
            c.order_uuid = (order_uuid,)
            c.deliv_addr = (deliv_addr,)
            c.client_id = client_id
            c.from_t = (deliv_time_from,)
            c.to_t = (deliv_time_to,)
            session.commit()

            answ_msg["reserved"] = True
            answ_msg["state"] = "Courier reserved"
            logger.info(f"courier_id={c.courier_id} sheduled for the {order_uuid=}")
            return True

    def cancel_reserved(
        self,
        event_id: int,
        order_uuid: str,
        answ_msg: dict,
    ) -> Optional[Courier]:
        logger.info("cancel_reserved()")
        answ_msg["canceled"] = False

        with SessionLocal() as session:
            c = session.query(Courier).filter(Courier.order_uuid == order_uuid).first()
            if c is None:
                answ_msg["state"] = "Not found the courier for that order"
                logger.info(f"Not found the courier for the order {order_uuid}")
                return False

            c.reserve_uuid = (event_id,)
            c.order_uuid = ("",)
            c.deliv_addr = ("",)
            c.client_id = (None,)
            c.from_t = (datetime.min,)
            c.to_t = (datetime.min,)
            session.commit()

            logger.info(f"courier_id={c.courier_id} canceled for the {order_uuid=}")
            answ_msg["canceled"] = True
            return True


logistic_utils = LogisticUtils()
