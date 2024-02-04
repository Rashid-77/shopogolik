from datetime import datetime
from typing import Optional
from pydantic import BaseModel


# Shared properties
class BalanceBase(BaseModel):
    user_id: int
    balance: Optional[float] = 0
    amount: Optional[float] = 0
    order_uuid: Optional[str] = ""
    depos_uuid: Optional[str] = ""
    deposit: Optional[bool] = False
    withdraw: Optional[bool] = False
    refunding: Optional[bool] = False


# Properties to receive via API on creation
class BalanceCreate(BalanceBase):
    pass


# Properties to receive via API on update
class BalanceUpdate(BalanceBase):
    pass

class BalanceNow(BaseModel):
    user_id: int
    balance: float

class BalanceInDBBase(BalanceBase):
    id: Optional[int] = None
    updDate : Optional[datetime] = None

    # class Config:
    #     orm_mode = True


# Additional properties to return via API
class Balance(BalanceInDBBase):
    pass
