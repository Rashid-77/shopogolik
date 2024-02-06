from sqlalchemy import Column, DateTime, Integer, Text ,DATETIME
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import relationship

from db import Base


class Courier(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, 
        ForeignKey('User.id', ondelete='CASCADE')
    )
    from_t = Column(DATETIME, default=0)
    to_t = Column(DATETIME, default=0)
    order_uuid = Column(Text, default="")
    deliv_addr = Column(Text, default="")
    user = relationship('User', backref='courier')
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False, 
        index=True, 
        default=None
        )
