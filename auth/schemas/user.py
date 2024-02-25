from typing import Annotated, Optional

from pydantic import BaseModel, Field, StringConstraints


# Shared properties
class UserBase(BaseModel):
    username: Annotated[str, StringConstraints(max_length=256)]
    first_name: Optional[str] = Field(None)
    last_name: Optional[str] = Field(None)
    email: str
    phone: Optional[str] = Field(None)


# Properties to receive via API on creation
class UserCreate(UserBase):
    username: str
    is_superuser: bool
    password: str
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
    is_superuser: bool
