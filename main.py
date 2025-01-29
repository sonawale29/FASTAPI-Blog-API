from fastapi import FastAPI,status,Depends,HTTPException
from schemas import Blogs,BlogsResponse
import models
from database import engine,get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post('/blogs/', status_code=status.HTTP_201_CREATED, response_model=BlogsResponse)
def create_blogs(blogs: Blogs,db: Session = Depends(get_db)):
    new_blogs = models.Blogs(title=blogs.title,content=blogs.content)
    db.add(new_blogs)
    db.commit()
    db.refresh(new_blogs)
    return new_blogs


@app.get('/blogs/{id}', status_code=status.HTTP_200_OK, response_model=BlogsResponse)
def get_blog(id: int, db: Session = Depends(get_db)):
    get_blog = db.query(models.Blogs).filter(models.Blogs.id == id).first()
    if not get_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blogs not found with id={id}")
    return get_blog


@app.delete('/blogs/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blogs).filter(models.Blogs.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blogs not found with id={id}")
    db.delete(blog)
    db.commit()


@app.put('/blogs/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=BlogsResponse)
def update_blog(id: int,request:Blogs,  db: Session = Depends(get_db)):
    blog = db.query(models.Blogs).filter(models.Blogs.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blogs not found with id={id}")

    blog.title = request.title
    blog.content = request.content
    db.commit()
    db.refresh(blog)
    return blog
