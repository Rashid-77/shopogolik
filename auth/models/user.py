from sqlalchemy import Boolean, Column, Integer, String

from db import Base


class User(Base):
    id = Column(Integer, primary_key=True)
    username = Column(String)#, length=256)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    hashed_password = Column(String)
    disabled = Column(Boolean)
    is_superuser = Column(Boolean, default=False)
