from typing import Annotated, Optional

from pydantic import BaseModel, StringConstraints


# Shared properties
class UserBase(BaseModel):
    user_id: Optional[int] = 1
    username: Annotated[str, StringConstraints(max_length=256)]
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: str
    phone: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
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
    is_superuser: bool
