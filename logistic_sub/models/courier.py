from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, Text ,DATETIME
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import relationship

from db import Base
from models.user import User


class Courier(Base):
    id = Column(Integer, primary_key=True)
    courier_id = Column(
        Integer, 
        ForeignKey('User.id', ondelete='CASCADE')
    )
    from_t = Column(DATETIME, default=datetime.min)
    to_t = Column(DATETIME, default=datetime.min)
    order_uuid = Column(Text, default="")
    deliv_addr = Column(Text, default="")
    client_id = Column(Integer, default=0)
    reserve_uuid = Column(Integer, default=0)
    user = relationship('User', backref='courier')
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False, 
        index=True, 
        default=None
        )
