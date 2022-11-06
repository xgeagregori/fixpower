from pydantic import BaseModel
from typing import Optional


class ProductListingBase(BaseModel):
    id: Optional[str]
    listed_price: float


class ProductListingCreate(ProductListingBase):
    pass


class ProductListingUpdate(ProductListingBase):
    pass
