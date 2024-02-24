from datetime import datetime

from db import Base
from sqlalchemy import DATETIME, Column, DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.orm import relationship


class Courier(Base):
    id = Column(Integer, primary_key=True)
    courier_id = Column(Integer, ForeignKey("User.id", ondelete="CASCADE"), unique=True)
    from_t = Column(DATETIME, default=datetime.min)
    to_t = Column(DATETIME, default=datetime.min)
    order_uuid = Column(Text, default="")
    deliv_addr = Column(Text, default="")
    client_id = Column(Integer, default=0)
    reserve_uuid = Column(Text, default="")
    user = relationship("User", backref="courier")
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
        default=None,
    )
