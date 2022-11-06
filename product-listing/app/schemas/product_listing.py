from pydantic import BaseModel
from typing import Optional


class ProductListingBase(BaseModel):
    listed_price: float


class ProductListingCreate(ProductListingBase):
    id: Optional[str]


class ProductListingUpdate(ProductListingBase):
    listed_price: Optional[float]
