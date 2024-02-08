from sqlalchemy import Column, DateTime, Integer, Boolean
from sqlalchemy.sql import func

from db import Base


class PubEvent(Base):
    id = Column(Integer, primary_key=True)
    delivered = Column(Boolean, default=False)
    deliv_fail = Column(Boolean, default=False)
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False, 
        index=True, 
        default=None
        )
