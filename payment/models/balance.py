from sqlalchemy import Boolean, Column, DateTime, Integer, Float, Text
from sqlalchemy import func

from db import Base


class Balance(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    balance = Column(Float, default=0)
    amount = Column(Float, default=0)
    order_uuid = Column(Text, default=0)
    depos_uuid = Column(Text, default=0)
    deposit = Column(Boolean, default=False)
    withdraw = Column(Boolean, default=False)
    refunding = Column(Boolean, default=False)
    updDate = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False, 
        index=True, 
        default=None
        )
