from pydantic import BaseModel
from typing import Optional


class ProductListingCreate(BaseModel):
    id: Optional[str]
    listed_price: float


class ProductListingUpdate(BaseModel):
    listed_price: Optional[float]
