from uuid import UUID
from sqlalchemy import Boolean, Column, Date, Integer, String, Text, Float, Uuid

from db import Base


class Order(Base):
    id = Column(Integer, primary_key=True)
    uuid = Column(Uuid)
    userId = Column(Integer)
    goods_reserved = Column(Boolean, default=False)
    money_reserved = Column(Boolean, default=False)
    courier_reserved = Column(Boolean, default=False)
