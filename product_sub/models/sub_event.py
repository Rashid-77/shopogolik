from sqlalchemy import Column, Integer

from db import Base


class SubEvent(Base):
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
