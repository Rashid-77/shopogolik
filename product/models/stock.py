import enum

from sqlalchemy import Column, Date, Integer, Enum, DateTime
from sqlalchemy.sql import func

from db import Base


class Stock(Base):
    id = Column(Integer, primary_key=True)
    prod_id = Column(Integer)
    updDate = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False, 
        index=True, 
        default=None
        )
    amount = Column(Integer)


class ProductState(enum.Enum):
    ''' the product is out of stock '''
    OUT_OF_STOCK = 0
    ''' the product in the stock '''
    IN_STOCK = 1
    ''' the product is reserved for customer, until payment succeeds '''
    RESERVED = 2
    ''' order is canceled, the product is returned to the stock '''
    CANCELED = 3
    ''' payment completed successfully, product is ready for packaging 
        and delivery to the courier '''
    SHIPPED = 4


class StockProdReservation(Base):
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer)
    prod_id = Column(Integer)
    amount = Column(Integer)
    updDate = Column(Date)
    state = Column(Enum(ProductState), default=0)
