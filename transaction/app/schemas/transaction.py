from pydantic import BaseModel
from typing import Optional


class TransactionBase(BaseModel):
    id: str
    state: str

class TransactionCreate(BaseModel):
    id: Optional[str]
    state: str
    
class TransactionUpdate(BaseModel):
    state: Optional[str]
    
class TransactionID(BaseModel):
    id: str
