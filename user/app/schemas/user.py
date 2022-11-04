from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    id: Optional[str]
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    id: str
    hashed_password: str
