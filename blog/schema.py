from pydantic import BaseModel
from typing import List, Optional

class Blog(BaseModel):
    title: str
    body: str

class User(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        from_attributes = True

class ShowUser(BaseModel):
    username: str
    email: str
    blogs: list[Blog] = []

    class Config:
        from_attributes = True 

class ShowBlog(Blog):
    title: str
    body: str
    creator: ShowUser
    
    class Config:
        from_attributes = True 

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None