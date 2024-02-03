from datetime import datetime
from typing import Optional

from pydantic import BaseModel
import enum

# Shared properties
class ReserveBase(BaseModel):
    order_event_id : Optional[int]
    order_id : Optional[str]
    prod_id : Optional[int] = 0
    to_reserve : Optional[int] = 0
    cancel : Optional[bool] = False
    state: Optional[enum.Enum]                # event_received, reserved, canceled, answer_sent
    amount_processed: Optional[int] = 0

# Properties to receive via API on creation
class ReserveCreate(ReserveBase):
    pass


# Properties to receive via API on update
class ReserveUpdate(ReserveBase):
    state: enum.Enum


class StockInDBBase(ReserveBase):
    id: int
    updDate : Optional[datetime] = None

    # class Config:
    #     orm_mode = True


# Additional properties to return via API
class Stock(StockInDBBase):
    pass
