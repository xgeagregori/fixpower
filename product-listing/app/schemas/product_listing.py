from pydantic import BaseModel
from typing import Optional
from app.schemas.product import ProductCreate


class ProductListingCreate(BaseModel):
    id: Optional[str]
    listed_price: float
    product: ProductCreate


class ProductListingUpdate(BaseModel):
    listed_price: Optional[float]
