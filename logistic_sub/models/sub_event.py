from db import Base
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func


class SubEvent(Base):
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    order_id = Column(String)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
        default=None,
    )
