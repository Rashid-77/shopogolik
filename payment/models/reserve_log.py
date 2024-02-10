import enum

from sqlalchemy import Column, Boolean, Integer, Enum, DateTime, String
from sqlalchemy.sql import func

from db import Base


class MoneyReserveState(enum.Enum):
    ''' defailt state '''
    NOT_DEFINED = 0
    ''' event just committed, and not processed yet'''
    EVENT_COMMIT = 1
    ''' the money is fully withdrawed from customer account '''
    RESERVED = 2
    ''' the balance is insufficient '''
    NOT_ENOUGH = 3
    ''' order is canceled, the product is returned to the stock '''
    CANCELED = 4


class MoneyReserve(Base):
    id = Column(Integer, primary_key=True)
    order_event_id = Column(Integer)
    order_id = Column(String)
    to_reserve = Column(Integer)
    cancel = Column(Boolean)
    state = Column(Enum(MoneyReserveState), default=MoneyReserveState.NOT_DEFINED)
    amount_processed = Column(Integer)
    updDate = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False, 
        index=True, 
        default=None
        )
