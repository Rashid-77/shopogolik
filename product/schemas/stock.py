from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class StockBase(BaseModel):
    prod_id : Optional[int]
    amount : Optional[int]
    reserved : Optional[int]

# Properties to receive via API on creation
class StockCreate(StockBase):
    prod_id: int


# Properties to receive via API on update
class StockUpdate(StockBase):
    pass

class StockInDBBase(StockBase):
    id: int
    updDate : Optional[datetime] = None

    # class Config:
    #     orm_mode = True


# Additional properties to return via API
class Stock(StockInDBBase):
    pass
