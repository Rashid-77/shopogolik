from datetime import datetime
from typing import Optional
from pydantic import BaseModel


# Shared properties
class PubEventBase(BaseModel):
    event_id: Optional[int] = None
    order_id: Optional[str] = None
    delivered: Optional[bool] = False
    deliv_fail: Optional[bool] = False


# Properties to receive via API on creation
class PubEventCreate(PubEventBase):
    pass


# Properties to receive via API on update
class PubEventUpdate(PubEventBase):
    delivered: bool
    deliv_fail: bool


class PubEventInDBBase(PubEventBase):
    id: Optional[int] = None
    updDate : Optional[datetime] = None

    # class Config:
    #     orm_mode = True


# Additional properties to return via API
class PubEvent(PubEventInDBBase):
    pass
