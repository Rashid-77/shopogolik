from sqlalchemy import Column, Date, Integer

from db import Base


class SubProdEvent(Base):
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    updDate = Column(Date)


class SubPaymEvent(Base):
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    updDate = Column(Date)
