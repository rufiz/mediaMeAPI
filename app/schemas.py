from typing import Optional, List
from datetime import datetime
import re

from pydantic import BaseModel, validator


class CommentBase(BaseModel):
    content: str
    post_id: int


class CommentDB(CommentBase):
    pass


class CommentOut(CommentBase):
    id: int
    user_id: int
    publication_date: datetime

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    content: str


class PostDB(PostBase):
    pass


class PostOut(PostBase):
    id: int
    user_id: int
    publication_date: datetime
    comments: List[CommentOut]

    class Config:
        orm_mode = True


class PostPartialUpdate(PostBase):
    title: Optional[str]
    content: Optional[str]


class UserBase(BaseModel):
    email: str


class UserIn(UserBase):
    password: str

    @validator('email')
    def is_email(cls, email):
        if not re.fullmatch(r'[^@]+@[^@]+\.[^@]+', email):
            raise ValueError('Invalid email.')
        return email

    @validator('password')
    def validate_password(cls, password):
        if len(password) < 8:
            raise ValueError('Password should be at least 8 characters.')
        return password


class UserDB(UserBase):
    hashed_password: str


class UserOut(UserBase):
    id: int
    email: str
    created_at: datetime
    posts: List[PostOut]

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
