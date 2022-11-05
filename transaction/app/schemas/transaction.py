from pydantic import BaseModel
from typing import Optional


class TransactionBase(BaseModel):

    state: str


class TransactionCreate(TransactionBase):
    id: Optional[str]
    state: str


class TransactionUpdate(BaseModel):
    state: Optional[str]
