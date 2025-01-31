from fastapi import FastAPI
from .database import engine
from app import models
from app.routers.users import user_router
from app.routers.blogs import blog_router
from app.routers.auth import auth_router


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(blog_router)



