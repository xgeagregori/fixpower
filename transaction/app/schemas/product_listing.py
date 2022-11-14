from pydantic import BaseModel
from typing import Optional


class ProductListingCreate(BaseModel):
    id: str


class ProductListingOut(BaseModel):
    id: str
