from datetime import datetime
from typing import Optional
from pydantic import BaseModel


# Shared properties
class SubEventBase(BaseModel):
    event_id: Optional[int] = None


# Properties to receive via API on creation
class SubEventCreate(SubEventBase):
    event_id: int


# Properties to receive via API on update
class SubEventUpdate(SubEventBase):
    pass


class SubEventInDBBase(SubEventBase):
    id: Optional[int] = None
    event_id: Optional[int] = None

    # class Config:
    #     orm_mode = True


# Additional properties to return via API
class SubEvent(SubEventInDBBase):
    pass
