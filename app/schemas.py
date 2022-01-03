from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from pydantic.types import conint

# one model for each of the different requests. Create a "reference class"
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# Extend each class
class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class Post(PostBase):
    # here we control exactly what fields we get back from the request, apart from the other inhereted attributes
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

# Schema of the post with the number of votes
class PostOut(BaseModel):
    Post: Post  # the name of the class must be capitalized because sqlalchemy always returns it capitalized
    votes: int  # however the votes name is lowercase because it is returned like that

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)  # To enforce 0 or 1 (less or equal to 1)