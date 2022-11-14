from pydantic import BaseModel
from typing import Optional, Union

from app.schemas.product import (
    ComponentCreate,
    DamagedProductCreate,
    RefurbishedProductCreate,
    ProductOut,
)
from app.schemas.user import UserCreate, UserOut


class ProductListingCreate(BaseModel):
    id: Optional[str]
    product: Union[ComponentCreate, DamagedProductCreate, RefurbishedProductCreate]
    listed_price: float
    seller: UserCreate


class ProductListingUpdate(BaseModel):
    buyer: Optional[UserCreate]
    listed_price: Optional[float]


class ProductListingOut(BaseModel):
    id: str
    product: ProductOut
    listed_price: float
    seller: UserOut
    buyer: Optional[UserOut]
    offers: list
    sold: bool
