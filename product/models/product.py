import enum

from sqlalchemy import Boolean, Column, Date, Integer, Enum, String, Float, DECIMAL

from db import Base


class Product(Base):
    id = Column(Integer, primary_key=True)
    sku = Column(String)
    name = Column(String)
    price = Column(DECIMAL(8, 2))
    weight_kg = Column(Float)
    width_m = Column(Float)
    length_m = Column(Float)
    height_m = Column(Float)
    volume_m3 = Column(Float)
    carDescr = Column(String)
    shortDescr = Column(String)
    longDescr = Column(String)
    thumb = Column(String)
    image = Column(String)
    updDate = Column(Date)
    live = Column(Boolean)
    virtual = Column(Boolean)
    unlimited = Column(Boolean)
    location = Column(String)


class Warehouse(Base):
    id = Column(Integer, primary_key=True)
    prod_id = Column(Integer)
    updDate = Column(Date)
    amount = Column(Float)


class ProductState(enum.Enum):
    ''' the product is out of stock '''
    OUT_OF_STOCK = 0
    ''' the product in the warehouse '''
    IN_STOCK = 1
    ''' the product is reserved for customer, until payment succeeds '''
    RESERVED = 2
    ''' order is canceled, the product is returned to the warehouse '''
    CANCELED = 3
    ''' payment completed successfully, product is ready for packaging 
        and delivery to the courier '''
    SHIPPED = 4


class WarehouseProdReservation(Base):
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer)
    prod_id = Column(Integer)
    updDate = Column(Date)
    prod_state = Column(Enum(ProductState), default=0)
