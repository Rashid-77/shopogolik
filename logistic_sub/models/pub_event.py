from sqlalchemy import Column, Date, Integer, String, Boolean

from db import Base


class PubEvent(Base):
    id = Column(Integer, primary_key=True)
    order_id = Column(String)
    updDate = Column(Date)
    delivered = Column(Boolean, default=False)
    deliv_fail = Column(Boolean, default=False)