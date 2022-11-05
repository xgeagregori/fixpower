from pydantic import BaseModel
from typing import Optional

class ProductListingBase(BaseModel):
    id: Optional[str]
    listed_price: str


class ProductListingCreate(ProductListingBase):
    pass

class ProductListingUpdate(ProductListingBase):
    pass