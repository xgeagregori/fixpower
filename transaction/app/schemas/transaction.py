from pydantic import BaseModel
from typing import Optional


class TransactionBase(BaseModel):
    state: str


class TransactionCreate(TransactionBase):
    id: Optional[str]


class TransactionUpdate(TransactionBase):
    state: Optional[str]
