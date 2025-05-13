from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# User Schemas

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

# Token Schemas

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Todo Schemas

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    time_to_do: datetime

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    time_to_do: datetime
    is_completed: bool
    created_at: datetime

    class Config:
        orm_mode = True
