from sqlalchemy import Column, DateTime, Integer, Text
from sqlalchemy import func

from db import Base


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
