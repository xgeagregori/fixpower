from pydantic import BaseModel
from typing import Optional, Union
from app.schemas.product import (
    ComponentCreate,
    DamagedProductCreate,
    RefurbishedProductCreate,
    ProductOut,
)


class ProductListingCreate(BaseModel):
    id: Optional[str]
    listed_price: float
    product: Union[ComponentCreate, DamagedProductCreate, RefurbishedProductCreate]


class ProductListingUpdate(BaseModel):
    listed_price: Optional[float]


class ProductListingOut(BaseModel):
    id: str
    listed_price: float
    product: ProductOut
    offers: list
    sold: bool
