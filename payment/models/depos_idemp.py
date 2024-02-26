from db import Base
from sqlalchemy import Column, DateTime, Integer, Text, func


class deposidemp(Base):
    id = Column(Integer, primary_key=True)
    uuid = Column(Text, nullable=False, unique=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
        default=None,
    )
