from datetime import datetime
from unittest.mock import Base

from pydantic import BaseModel, EmailStr, Field, conint
from pydantic.config import ConfigDict
from typing_extensions import Annotated


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserBase(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class UserOut(UserBase):
    pass

    class Config:
        from_attributes = True


class UserProfileOut(BaseModel):
    id: int
    user_id: int
    username: str
    bio: str | None = None

    class Config:
        from_attributes = True


class Post(PostBase):
    id: int
    created_at: datetime
    author_id: int | None = None
    author: UserOut

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str
    bio: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserAndProfile(BaseModel):
    user: UserOut
    profile: UserProfileOut


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str | None = None


class Vote(BaseModel):
    post_id: int
    direction: Annotated[int, Field(strict=True, le=1)]
