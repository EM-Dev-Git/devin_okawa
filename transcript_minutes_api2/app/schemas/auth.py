from pydantic import BaseModel
from typing import Optional


class UserLogin(BaseModel):
    user_id: str
    password: str


class UserRegister(BaseModel):
    user_id: str
    password: str
    email: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[str] = None
