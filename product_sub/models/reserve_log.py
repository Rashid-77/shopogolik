import enum

from db import Base
from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String
from sqlalchemy.sql import func


class ProdReserveState(enum.Enum):
    NOT_DEFINED = 0
    """ event just committed, and not processed yet"""
    EVENT_COMMIT = 1
    """ the product is fully reserved for customer """
    RESERVED = 2
    """ the product partially reserved """
    PARTIALLY = 3
    """ the product out of stock"""
    OUT_OF_STOCK = 4
    """ stock has no such product id """
    BAD_PROD_ID = 5
    """ order is canceled, the product is returned to the stock """
    CANCELED = 6


class Reserve(Base):
    id = Column(Integer, primary_key=True)
    order_event_id = Column(Integer)
    order_id = Column(String)
    prod_id = Column(Integer)
    to_reserve = Column(Integer)
    cancel = Column(Boolean)
    state = Column(Enum(ProdReserveState), default=ProdReserveState.NOT_DEFINED)
    amount_processed = Column(Integer)
    updDate = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
        default=None,
    )
