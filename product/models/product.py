from sqlalchemy import Boolean, Column, Date, Integer, String, Float, DECIMAL

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
