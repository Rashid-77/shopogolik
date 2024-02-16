from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from db import Base


class SubUserEvent(Base):
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    user_id = Column(Integer)
    state = Column(String, default="")
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False, 
        index=True, 
        default=None
        )
