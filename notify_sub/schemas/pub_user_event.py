from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class PubUserEventBase(BaseModel):
    user_id: Optional[int] = None
    state: Optional[str] = ""
    delivered: Optional[bool] = False
    deliv_fail: Optional[bool] = False


# Properties to receive via API on creation
class PubUserEventCreate(PubUserEventBase):
    pass


# Properties to receive via API on update
class PubUserEventUpdate(PubUserEventBase):
    delivered: bool
    deliv_fail: bool


class PubUserEventInDBBase(PubUserEventBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    # class Config:
    #     orm_mode = True


# Additional properties to return via API
class PubUserEvent(PubUserEventInDBBase):
    pass
