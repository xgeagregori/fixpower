from pydantic import BaseModel


class ProductListingCreate(BaseModel):
    id: str


class ProductListingOut(BaseModel):
    id: str
