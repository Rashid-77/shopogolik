from db import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text, Uuid, func
from sqlalchemy.orm import relationship


class Notify(Base):
    id = Column(Integer, primary_key=True)
    order_uuid = Column(Uuid, default="")
    client_id = Column(Integer, ForeignKey("User.id", ondelete="CASCADE"), unique=True)
    msg = Column(Text, default="")
    delivered = Column(Boolean, default=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
        default=None,
    )
    user = relationship("User", backref="courier")
