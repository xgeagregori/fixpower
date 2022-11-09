from pydantic import BaseModel
from typing import Optional


class TransactionCreate(BaseModel):
    id: Optional[str]
    state: str


class TransactionUpdate(BaseModel):
    state: Optional[str]
