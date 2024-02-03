from typing import Optional
from sqlalchemy import and_
from sqlalchemy.orm import Session

from pydantic import BaseModel

from db.session import SessionLocal
from models.stock import Stock
from models.reserve_log import Reserve, ProdReserveState
from crud.crud_stock import stock
from utils.log import get_console_logger

logger = get_console_logger(__name__)

def prod_reserve_msg(state: ProdReserveState):
    if state == ProdReserveState.NOT_DEFINED:
        return "not_defined"
    elif state == ProdReserveState.EVENT_COMMIT:
        return "event_commit"
    elif state == ProdReserveState.RESERVED:
        return "full_reserved"
    elif state == ProdReserveState.PARTIALLY:
        return "part_reserved"
    elif state == ProdReserveState.OUT_OF_STOCK:
        return "out_of_stock"
    elif state == ProdReserveState.CANCELED:
        return "canceled"
    elif state == ProdReserveState.BAD_PROD_ID:
        return "bad_prod_id"
    else:
        return "not implemented"



class StockUtils:

    def reserve_product(
            self, 
            prod_id: int, 
            amount,
        ):
        ''' 
        It reserves the "amount" of products in stock
        and returns the number of reserved products, and state of the reservation.
        '''
        logger.info("reserve_product()")
        with SessionLocal() as session:
            db_obj: Stock = session.query(Stock).filter(Stock.prod_id == prod_id).first()
            if db_obj is None:
                return 0, ProdReserveState.BAD_PROD_ID # reserve_state.bad_prod_id
            amount_now = db_obj.amount

            if amount_now <= 0:
                return reserved, ProdReserveState.OUT_OF_STOCK #reserve_state.fail
            
            if amount_now >= amount:
                obj_in={"amount": amount_now - amount}
                reserved, msg = amount, ProdReserveState.RESERVED #  reserve_state.fully
            else:
                obj_in={"amount": 0}
                reserved, msg = amount_now, ProdReserveState.PARTIALLY # reserve_state.partially

            session.add(db_obj)
            stock.update_without_commit(session, db_obj=db_obj, obj_in=obj_in)
            session.commit()
        return reserved, msg


    def cancel_reserved(self, order_id: str) -> Optional[Stock]:
        logger.info("cancel_reserved()")
        with SessionLocal() as session:
            cancel_cmd = session.query(Reserve) \
                                .filter(
                                    and_(
                                        Reserve.order_id==order_id, 
                                        Reserve.cancel==True
                                        )).order_by(Reserve.updDate.desc()).all()
            if len(cancel_cmd) > 1:
                logger.warning(" Found duplicate cancel command. The last'll be used")
            cancel_cmd = cancel_cmd[0]
            
            if cancel_cmd.state == ProdReserveState.CANCELED:
                logger.warn(f" Found duplicate cancel command for reserved products. {order_id=}")
                return   # reserve already canceled
            
            prods = session.query(Reserve) \
                            .filter(
                                and_(
                                    Reserve.order_id == order_id,
                                    Reserve.cancel==False
                                    )) \
                            .order_by(Reserve.prod_id) \
                            .all()
            
            prod_ids = [p.prod_id for p in prods]
            prod_in_stock = session.query(Stock) \
                                .filter(Stock.prod_id.in_(prod_ids)) \
                                .order_by(Stock.prod_id) \
                                .all()
            logger.info(f' {order_id=}')
            for p in prods:
                for ps in prod_in_stock:
                    if p.prod_id != ps.prod_id:
                        continue
                    if p.to_reserve >= 0:
                        before = ps.amount
                        ps.amount += p.to_reserve
                        logger.info(f'  stock: {p.prod_id=}, {before=}, now={ps.amount}')
                        p.state = ProdReserveState.CANCELED
            cancel_cmd.state = ProdReserveState.CANCELED
            session.add_all(prods)
            session.add_all(prod_in_stock)
            session.add(cancel_cmd)
            session.commit()
            # check
            prod_in_stock = session.query(Stock) \
                                .filter(Stock.prod_id.in_(prod_ids)) \
                                .order_by(Stock.prod_id) \
                                .all()
            for p in prod_in_stock:
                logger.info(f' stock_sql: {p.prod_id=}, now={p.amount}')
            return


stock_utils = StockUtils()
