from datetime import date
from typing import Optional

from pydantic import BaseModel, NameEmail, Field
from pydantic_extra_types.phone_numbers import PhoneNumber

# Shared properties
class UserBase(BaseModel):
    username: Optional[str] = Field(None, max_legth=256)
    first_name: str
    last_name: str
    email: str#NameEmail
    phone: str#PhoneNumber


# Properties to receive via API on creation
class UserCreate(UserBase):
    username: str
    # password: str
    # is_superuser: bool = False
    pass


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    # class Config:
    #     orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
