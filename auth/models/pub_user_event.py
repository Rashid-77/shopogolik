from sqlalchemy import Column, DateTime, Integer, Boolean, String
from sqlalchemy.sql import func

from db import Base


class PubUserEvent(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    state = Column(String, default="")
    delivered = Column(Boolean, default=False)
    deliv_fail = Column(Boolean, default=False)
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False, 
        index=True, 
        default=None
        )
