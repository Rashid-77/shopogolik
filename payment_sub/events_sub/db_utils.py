from decimal import Decimal
from typing import Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy import and_
from db.session import SessionLocal
from models.balance import Balance
from schemas.balance import BalanceCreate, BalanceUpdate
from logger import logger


class BalanceUtils():

    def reserve_money(
            self, 
            event_id: int, 
            user_id: int, 
            order_uuid: str, 
            amount: Decimal, 
            answ_msg: dict
        ) -> bool:
        ''' 
        It reserves the "amount" of money in balance table
        and returns the amount of reserved money, and state of the reservation.
        '''
        logger.info("reserve_money()")
        with SessionLocal() as session:
            bal = session.query(Balance) \
                            .filter(
                                and_(
                                    Balance.user_id == user_id,
                                    Balance.order_uuid == order_uuid,
                                    Balance.reserve == True,
                                    Balance.success == True
                                )
                            ) \
                            .all()
            if len(bal):
                # exit, reservation already done
                answ_msg["reserved"] = False
                answ_msg["state"] = 'already reserved'
                logger.info(f'Money for the order {order_uuid}) already reserved')
                return False
            
            bal = session.query(Balance) \
                            .filter(Balance.user_id == user_id) \
                            .order_by(Balance.created_at.desc()).first()

            if bal is None:
                answ_msg["reserved"] = False
                answ_msg["state"] = 'user has no incomes (balance=0)'
                logger.info(f'User_id {user_id} has no balance records')
                return False

            new_bal = Balance(
                user_id = user_id,
                order_uuid = order_uuid,
                reserve_uuid = event_id,
                balance = bal.balance,
                amount = amount,
                reserve = True,
            )
            new_balance = Decimal(bal.balance) - amount
            
            if new_balance < Decimal("0.00"):
                logger.info('Balance is insufficient')
                answ_msg["reserved"] = False
                answ_msg["state"] = 'Balance is insufficient'
                res = False
            else:
                logger.info(f' user balance: {bal.balance} - {amount} = {new_balance}')
                new_bal.success = True
                new_bal.balance = new_balance
                answ_msg["reserved"] = True
                answ_msg["state"] = 'Money reserved'
                res = True
            
            session.add(new_bal)
            session.commit()
            
            return res


    def cancel_reserved(
            self, 
            event_id: int, 
            user_id: int, 
            order_uuid: str, 
            answ_msg: dict,
        ) -> bool:
        logger.info("cancel_reserved()")
        answ_msg["canceled"] = False
        with SessionLocal() as session:
            bal = session.query(Balance) \
                            .filter(
                                and_(
                                    Balance.order_uuid == order_uuid,
                                    Balance.refunding == True,
                                    Balance.success == True
                                )
                            ) \
                            .all()
            if len(bal):
                # exit, refunding already done
                answ_msg["state"] = 'already refunded'
                logger.info(f'Money for the order {order_uuid}) already reserved')
                return False
            
            bal = session.query(Balance) \
                            .filter(
                                and_(
                                    Balance.order_uuid == order_uuid,
                                    Balance.reserve == True
                                )
                            ) \
                            .order_by(Balance.created_at.desc()).first()
            if bal is None:
                answ_msg["state"] = 'user has no reservation'
                logger.info(f'{order_uuid} has no reservation')
                return False

            if not bal.success:
                # last reservation was unsuccessfull and nothing to refund and public
                return False

            new_balance = bal.balance + bal.amount
            if new_balance < Decimal("0.00") or new_balance < bal.balance:
                bal.success = False
                answ_msg["state"] = 'new_balance try to be negative'
                logger.info(f'New balance try to be negative. {order_uuid=} '
                            f'{bal.balance} + {bal.amount} = {new_balance} ')
                return True

            new_bal = Balance(
                user_id = user_id,
                order_uuid = order_uuid,
                refund_uuid = event_id,
                balance = new_balance,
                amount = bal.amount,
                refunding = True,
                success = True
            )
            logger.info(f' user balance: {bal.balance} + {bal.amount} = {new_balance}')
            session.add(new_bal)
            session.commit()
            answ_msg["canceled"] = True
            answ_msg["state"] = "money refunded"
            return True


balance_utils = BalanceUtils()
