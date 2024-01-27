from sqlalchemy import Boolean, Column, Date, Integer, String, Text, Float

from db import Base


class Product(Base):
    id = Column(Integer, primary_key=True)
    sku = Column(String)
    name = Column(String)
    price = Column(Float)
    weight = Column(Float)
    carDescr = Column(String)
    shortDescr = Column(String)
    longDescr = Column(String)
    thumb = Column(String)
    image = Column(String)
    updDate = Column(Date)
    stock = Column(Float)
    Live = Column(Boolean)
    unlimited = Column(Boolean)
    location = Column(String)
