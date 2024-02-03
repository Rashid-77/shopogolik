from sqlalchemy import Column, Integer, Date, String

from db import Base


class SubEvent(Base):
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    order_id = Column(String)
    updDate = Column(Date)
