from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


# Shared properties
class OrderBase(BaseModel):
    uuid: Optional[UUID] = None
    userId: int
    goods_reserved: bool = Field(default=False)
    money_reserved: bool = Field(default=False)
    courier_reserved: bool = Field(default=False)
    reserv_user_canceled: bool = Field(default=False)
    goods_fail: bool = Field(default=False)
    money_fail: bool = Field(default=False)
    courier_fail: bool = Field(default=False)


# Properties to receive via API on creation
class OrderCreate(OrderBase):
    uuid: UUID


# Properties to receive via API on update
class OrderUpdate(OrderBase):
    pass


class OrderInDBBase(OrderBase):
    id: Optional[int] = None

    # class Config:
    #     orm_mode = True


# Additional properties to return via API
class Order(OrderInDBBase):
    pass
