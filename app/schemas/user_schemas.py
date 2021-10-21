from typing import Optional
import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    username: str


class UserPatchUpdate(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


class User(UserBase):
    id: int
    username: str
    register_date: datetime.datetime

    class Config:
        orm_mode = True
