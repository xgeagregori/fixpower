from pydantic import BaseModel


class UserCreate(BaseModel):
    id: str

class UserOut(BaseModel):
    id: str
