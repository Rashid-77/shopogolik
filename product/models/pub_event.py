from db import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func


class PubEvent(Base):
    id = Column(Integer, primary_key=True)
    order_id = Column(String)
    delivered = Column(Boolean, default=False)
    deliv_fail = Column(Boolean, default=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
        default=None,
    )
