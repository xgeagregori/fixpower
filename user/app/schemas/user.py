from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    id: Optional[str]
    username: str
    email: str
    password: str
    is_admin: Optional[bool]


class UserUpdate(BaseModel):
    email: Optional[str]
    password: Optional[str]


class UserInDB(BaseModel):
    id: str
    username: str
    email: str
    hashed_password: str
    is_admin: Optional[bool]


class UserOut(BaseModel):
    id: str
    username: str
    email: str
    is_admin: bool
