from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class User(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    role: str = "user"
    profile_picture: Optional[str] = None
    created_at: datetime = datetime.utcnow()

class UserInDB(User):
    id: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class Ad(BaseModel):
    title: str
    description: str
    category: str
    location: str
    age: Optional[int] = None
    contact_info: Optional[str] = None
    images: List[str] = []
    user_id: str
    created_at: datetime = datetime.utcnow()
    approved: bool = False
    views: int = 0

class AdInDB(Ad):
    id: str

class AdCreate(BaseModel):
    title: str
    description: str
    category: str
    location: str
    age: Optional[int] = None
    contact_info: Optional[str] = None
    images: List[str] = []

class AdUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    age: Optional[int] = None
    contact_info: Optional[str] = None
    images: Optional[List[str]] = None
