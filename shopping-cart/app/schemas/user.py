from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    id: str


class UserOut(BaseModel):
    id: str
