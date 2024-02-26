from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class OrderInfoBase(BaseModel):
    uuid: UUID
    userId: int
    products: list
    total_price: Decimal
    deliv_addr: str
    deliv_t_from: datetime
    deliv_t_to: datetime


# Properties to receive via API on creation
class OrderInfoCreate(OrderInfoBase):
    pass


# Properties to receive via API on update
class OrderInfoUpdate(OrderInfoBase):
    pass


class OrderInfoInDBBase(OrderInfoBase):
    id: Optional[int] = None

    # class Config:
    #     orm_mode = True


# Additional properties to return via API
class OrderInfo(OrderInfoInDBBase):
    pass
