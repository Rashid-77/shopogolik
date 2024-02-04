from typing import Optional
from sqlalchemy import and_

from db.session import SessionLocal
from models.stock import Stock
from models.reserve_log import Reserve, ProdReserveState
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
    msg_reserved = prod_reserve_msg(ProdReserveState.RESERVED)
    msg_partially = msg_out_of = prod_reserve_msg(ProdReserveState.PARTIALLY)
    msg_out_of_stock = prod_reserve_msg(ProdReserveState.OUT_OF_STOCK)

    def reserve_product(
            self, 
            event_id: int, 
            order_uuid: str, 
            products: dict, 
            answ_msg: dict
        ):
        ''' 
        It reserves the "amount" of products in stock
        and returns the number of reserved products, and state of the reservation.
        '''
        logger.info("reserve_product()")
        prod_ids = [p.get("prod_id") for p in products]
        reserved = []
        cnt_full, cnt_fail = 0, 0
        with SessionLocal() as session:
            prod_in_stock = session.query(Stock) \
                                .filter(Stock.prod_id.in_(prod_ids)) \
                                .order_by(Stock.prod_id) \
                                .all()
            logger.info(f'-----------------')
            for p in products:
                p_id = p.get("prod_id")
                amount = p.get("amount")
                logger.info(f'>{p_id=}, {amount=}')
                r=Reserve(
                    order_event_id=event_id,
                    order_id=order_uuid,
                    prod_id=p_id,
                    to_reserve=amount,
                    cancel=False,
                    state=ProdReserveState.EVENT_COMMIT,
                    amount_processed=0
                )
                res = {"prod_id": r.prod_id, "amount": 0}
                r.amount_processed
                for ps in prod_in_stock:
                    logger.info(f' {p_id} ? {ps.prod_id}')
                    if p_id != ps.prod_id:
                        logger.info(f'  continue')
                        continue

                    amount_now = ps.amount
                    logger.info(f'  {amount_now=}')
                    if amount_now <= 0:
                        r.state = ProdReserveState.OUT_OF_STOCK
                        res["msg"] = self.msg_out_of_stock
                        cnt_fail += 1
                        logger.info(f'  OUT_OF_STOCK')
                        break

                    if amount_now >= amount:
                        ps.amount = amount_now - amount
                        r.amount_processed = amount
                        r.state = ProdReserveState.RESERVED
                        res["amount"] = amount
                        res["msg"] = self.msg_reserved
                        cnt_full += 1
                        logger.info(f'  RESERVED')
                    else:
                        ps.amount = 0
                        r.amount_processed = amount_now
                        r.state = ProdReserveState.PARTIALLY
                        res["amount"] = amount_now
                        res["msg"] = self.msg_partially
                        logger.info(f'  PARTIALLY')
                    logger.info(f'  stock={ps.amount}, reserved={r.amount_processed}, st={r.state}')
                    break
                
                answ_msg["reserved"].append(res)
                
                if r.state == ProdReserveState.EVENT_COMMIT:
                    r.state == ProdReserveState.BAD_PROD_ID
                    logger.info(f'  BAD_PROD_ID')

                reserved.append(r)
                logger.info(f"{len(reserved)=}")
            
            session.add_all(reserved)
            logger.info("add_all(reserved)")
            
            session.add_all(prod_in_stock)
            logger.info("add_all(prod_in_stock)")
            
            session.commit()
            logger.info("commit")
            # check
            prod_in_stock = session.query(Stock) \
                                .filter(Stock.prod_id.in_(prod_ids)) \
                                .order_by(Stock.prod_id) \
                                .all()
            logger.info(f'------ check -------')
            for p in prod_in_stock:
                logger.info(f' stock_sql: {p.prod_id=}, now={p.amount}')

            logger.info(f'-----------------')
        return cnt_full, cnt_fail


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
                    if p.amount_processed >= 0:
                        before = ps.amount
                        ps.amount += p.amount_processed
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
