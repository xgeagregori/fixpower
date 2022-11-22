from pydantic import BaseModel
from typing import Optional


class ItemCreate(BaseModel):
    id: str


class ItemOut(BaseModel):
    id: str
