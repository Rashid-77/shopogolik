'''
    The limited version of user schemas from auth service.
    It does not have hashed password
'''

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

# Shared properties
class UserBase(BaseModel):
    user_id: Optional[int]
    username: Optional[str] = Field(None, max_legth=256)
    first_name: Optional[str] = Field(None)
    last_name: Optional[str] = Field(None)
    email: str
    phone: Optional[str] = Field(None)


# Properties to receive via API on creation
class UserCreate(UserBase):
    user_id: int
    username: str
    is_superuser: bool


# Properties to receive via API on update
class UserUpdate(UserBase):
    pass


class UserInDBBase(UserBase):
    id: Optional[int] = None

    # class Config:
    #     orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    disabled: bool
    is_superuser: bool
