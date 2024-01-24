from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, NameEmail
from pydantic_extra_types.phone_numbers import PhoneNumber

# Shared properties
class OrderBase(BaseModel):
    uuid: Optional[UUID] = None
    userId: int
    shipName: str
    shipAddr: str
    city: str
    state: str
    zip: str
    country: str
    email: str
    phone: str
    tax: float


# Properties to receive via API on creation
class OrderCreate(OrderBase):
    uuid: UUID
    amount: float


# Properties to receive via API on update
class OrderUpdate(OrderBase):
    amount: float


class OrderShip(OrderBase):
    shiped: bool = Field(default=False)
    shipDate: datetime
    trackinNumber: str


class OrderInDBBase(OrderBase):
    id: Optional[int] = None

    # class Config:
    #     orm_mode = True


# Additional properties to return via API
class Order(OrderInDBBase):
    pass
