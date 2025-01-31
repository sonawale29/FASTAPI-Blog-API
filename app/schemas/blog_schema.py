from pydantic import BaseModel
from typing import List


class Blogs(BaseModel):
    title: str
    content: str


class BlogsResponse(Blogs):
    id: int = 1
    user_id: int = 1

    class Config:
        from_attributes = True
