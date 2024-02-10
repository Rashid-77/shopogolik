from sqlalchemy import Boolean, Column, DateTime, Integer, Float, Text, DECIMAL
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import relationship

from db import Base


class Balance(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    balance = Column(DECIMAL, default=0)
    amount = Column(DECIMAL, default=0)
    order_uuid = Column(Text, default="")
    deposit = Column(Boolean, default=False)
    reserve = Column(Boolean, default=False)
    withdraw = Column(Boolean, default=False)
    refunding = Column(Boolean, default=False)
    success = Column(Boolean, default=False)
    deposidemp_id = Column(
        Integer, 
        ForeignKey('deposidemp.id', ondelete='CASCADE')
    )
    deposidemp = relationship('deposidemp', backref='balance')
    reserve_uuid = Column(Text, default="")
    withdraw_uuid = Column(Text, default="")
    refund_uuid = Column(Text, default="")
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False, 
        index=True, 
        default=None
        )


class deposidemp(Base):
    id = Column(Integer, primary_key=True)
    uuid = Column(Text, nullable=False, unique=True)
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False, 
        index=True, 
        default=None
        )
