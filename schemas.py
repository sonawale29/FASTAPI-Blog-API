from pydantic import BaseModel


class Blogs(BaseModel):
    title: str
    content: str


class BlogsResponse(Blogs):
    id: int = 1

    class Config:
        from_attributes = True
