from datetime import datetime
from typing import Optional
from pydantic import BaseModel


# Shared properties
class CourierBase(BaseModel):
    from_t: Optional[datetime] = 0
    to_t: Optional[datetime] = 0
    order_uuid: Optional[str] = ""
    deliv_addr: Optional[str] = ""
    client_id: int
    reserve_uuid: int


# Properties to receive via API on creation
class CourierCreate(CourierBase):
    pass


# Properties to receive via API on update
class CourierUpdate(CourierBase):
    from_t: datetime
    to_t: datetime
    order_uuid: str
    deliv_addr: str
    client_id: int
    reserve_uuid: int

class CourierUnoccupied(BaseModel):
    id: Optional[int] = None
    courier_id: int


class CourierInDBBase(CourierBase):
    id: Optional[int] = None
    courier_id: int
    created_at : Optional[datetime] = None

    # class Config:
    #     orm_mode = True


# Additional properties to return via API
class Courier(CourierInDBBase):
    pass
