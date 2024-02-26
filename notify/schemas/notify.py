from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class NotifyBase(BaseModel):
    order_uuid: Optional[UUID] = ""
    client_id: Optional[int] = ""
    msg: Optional[str] = ""
    delivered: Optional[bool] = False


# Properties to receive via API on creation
class NotifyCreate(NotifyBase):
    pass


# Properties to receive via API on update
class NotifyUpdate(NotifyBase):
    order_uuid: str
    client_id: int
    msg: str


class NotifyInDBBase(NotifyBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    # class Config:
    #     orm_mode = True


# Additional properties to return via API
class Notify(NotifyInDBBase):
    pass
