from pydantic import BaseModel
from .blog_schema import BlogsResponse
from typing import List


class User(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int = 1
    username: str
    email: str

    class Config:
        from_attributes = True


class GetUser(BaseModel):
    id: int = 1
    username: str
    email: str
    blogs: List[BlogsResponse] = []

    class Config:
        from_attributes = True
