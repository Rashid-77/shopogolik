"""
    The limited version of user model from auth service.
    It does not have hashed password
"""
from db import Base
from sqlalchemy import Boolean, Column, Integer, String


class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    disabled = Column(Boolean)
    is_superuser = Column(Boolean, default=False)
