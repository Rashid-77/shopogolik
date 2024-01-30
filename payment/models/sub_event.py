from sqlalchemy import Column, Integer, Date

from db import Base


class SubEvent(Base):
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    updDate = Column(Date)
