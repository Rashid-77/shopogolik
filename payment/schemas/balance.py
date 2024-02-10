from datetime import datetime
from typing import Optional
from pydantic import BaseModel


# Shared properties
class BalanceBase(BaseModel):
    user_id: int
    balance: Optional[float] = 0
    amount: Optional[float] = 0
    deposit: Optional[bool] = False
    reserve: Optional[bool] = False
    withdraw: Optional[bool] = False
    refunding: Optional[bool] = False
    success: Optional[bool] = False
    order_uuid: Optional[str] = ""
    reserve_uuid: Optional[str] = ""
    withdraw_uuid: Optional[str] = ""
    refund_uuid: Optional[str] = ""


# Properties to receive via API on creation
class BalanceCreate(BalanceBase):
    depos_uuid: str

class BalanceWithdraw(BalanceBase):
    withdraw_uuid: str
    amount: float

# Properties to receive via API on update
class BalanceUpdate(BalanceBase):
    pass

class BalanceNow(BaseModel):
    user_id: int
    balance: float

class BalanceInDBBase(BalanceBase):
    id: Optional[int] = None
    deposidemp_id: int
    created_at : Optional[datetime] = None

    # class Config:
    #     orm_mode = True


# Additional properties to return via API
class Balance(BalanceInDBBase):
    pass
