from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from app.models import User
from app.database import get_db
from app.services.auth import hash_password
from app.schemas import user_schema
from fastapi.security import OAuth2PasswordBearer
from app.services.auth import decode_access_token
from app.services.user import get_user

user_router = APIRouter(tags=["User"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> user_schema.User:
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token")

    user = get_user(db, payload.username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user


@user_router.get("/users/me", response_model=user_schema.UserResponse)
def read_users_me(current_user: user_schema.User = Depends(get_current_user)):
    return current_user


@user_router.post('/user/', status_code=status.HTTP_201_CREATED, response_model=user_schema.UserResponse)
def create_user(user: user_schema.User, db: Session = Depends(get_db)):
    new_user = User(username=user.username, email=user.email, password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@user_router.get('/user/{id}', status_code=status.HTTP_200_OK, response_model=user_schema.GetUser)
def get_user_data(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with ID={id} not found")
    return user


