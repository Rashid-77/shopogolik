from sqlalchemy import Column, Date, Integer

from db import Base

# TODO refactor these models

class SubProdEvent(Base):
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    updDate = Column(Date)


class SubPaymEvent(Base):
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    updDate = Column(Date)


class SubLogisEvent(Base):
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    updDate = Column(Date)