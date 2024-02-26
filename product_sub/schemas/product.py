from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


# Shared properties
class ProductBase(BaseModel):
    sku: Optional[str] = None
    name: str
    price: Decimal
    weight_kg: Optional[float] = None
    width_m: Optional[float] = None
    length_m: Optional[float] = None
    height_m: Optional[float] = None
    volume_m3: Optional[float] = None
    carDescr: Optional[str] = None
    shortDescr: Optional[str] = None
    longDescr: Optional[str] = None
    thumb: Optional[str] = None
    image: Optional[str] = None
    live: Optional[bool] = False
    virtual: Optional[bool] = False
    unlimited: Optional[bool] = False
    location: Optional[str] = None


# Properties to receive via API on creation
class ProductCreate(ProductBase):
    pass


# Properties to receive via API on update
class ProductUpdate(ProductBase):
    pass


# class ProductShip(ProductBase):
#     pass


class ProductInDBBase(ProductBase):
    id: int
    updDate: Optional[datetime] = None

    # class Config:
    #     orm_mode = True


# Additional properties to return via API
class Product(ProductInDBBase):
    pass
