from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Post(BaseModel):
    title: str
    content: str
    published: bool 
    created_at:datetime
    user_id:int
    user: UserResponse

class PostResponse(BaseModel):
    Posts:Post
    votes:int

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    user_id: int
    username: Optional[str]

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)