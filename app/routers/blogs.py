from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from app.models import Blogs
from app.database import get_db
from app.schemas import blog_schema
from app.schemas import user_schema

from app.routers.users import get_current_user

blog_router = APIRouter(tags=["Blogs"])


@blog_router.post('/blogs/', status_code=status.HTTP_201_CREATED, response_model=blog_schema.BlogsResponse)
def create_blogs(blogs: blog_schema.Blogs,db: Session = Depends(get_db),
    current_user: user_schema.UserResponse = Depends(get_current_user)):
    new_blogs = Blogs(title=blogs.title, content=blogs.content, user_id=current_user.id)
    db.add(new_blogs)
    db.commit()
    db.refresh(new_blogs)
    return new_blogs


@blog_router.get('/blogs/{id}', status_code=status.HTTP_200_OK, response_model=blog_schema.BlogsResponse)
def get_blog(id: int, db: Session = Depends(get_db),
             current_user: user_schema.UserResponse = Depends(get_current_user)):
    get_blog = db.query(Blogs).filter(Blogs.id == id).first()
    if not get_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blogs not found with id={id}")
    return get_blog


@blog_router.delete('/blogs/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db),
                current_user: user_schema.UserResponse = Depends(get_current_user)):
    blog = db.query(Blogs).filter(Blogs.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blogs not found with id={id}")
    db.delete(blog)
    db.commit()


@blog_router.put('/blogs/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=blog_schema.BlogsResponse)
def update_blog(id: int,request:blog_schema.Blogs,  db: Session = Depends(get_db),
                current_user: user_schema.UserResponse = Depends(get_current_user)):
    blog = db.query(Blogs).filter(Blogs.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blogs not found with id={id}")

    blog.title = request.title
    blog.content = request.content
    db.commit()
    db.refresh(blog)
    return blog
