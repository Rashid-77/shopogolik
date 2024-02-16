from datetime import datetime
from typing import Optional
from pydantic import BaseModel


# Shared properties
class SubUserEventBase(BaseModel):
    event_id: Optional[int] = None
    user_id: Optional[int] = None
    state: Optional[str] = ""


# Properties to receive via API on creation
class SubUserEventCreate(SubUserEventBase):
    event_id: int
    user_id: int
    state: str


# Properties to receive via API on update
class SubUserEventUpdate(SubUserEventBase):
    pass


class SubUserEventInDBBase(SubUserEventBase):
    id: Optional[int] = None
    event_id: Optional[int] = None
    created_at : Optional[datetime] = None

    # class Config:
    #     orm_mode = True


# Additional properties to return via API
class SubUserEvent(SubUserEventInDBBase):
    pass
