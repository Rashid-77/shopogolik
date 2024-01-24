from uuid import UUID
from sqlalchemy import Boolean, Column, Date, Integer, String, Text, Float, Uuid

from db import Base


class Order(Base):
    id = Column(Integer, primary_key=True)
    userId = Column(Integer)
    amount = Column(Float)
    shipName = Column(String)
    shipAddr = Column(String)
    city = Column(String)
    state = Column(String)
    zip = Column(String)
    country = Column(String)
    email = Column(String)
    phone = Column(String)
    tax = Column(Float)
    shiped = Column(Boolean, default=False)
    shipDate = Column(Date)
    trackinNumber = Column(String, default="")
